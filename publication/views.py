# Importation des modules nécessaires
import json
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from publication.models import Blogs, Tag, About, Contact, Comment, Discussion
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse

# Vue d'accueil
def home(request):
    return render(request, 'home.html')

# Gestion du blog avec recherche, tri et pagination
def handleblog(request):
    search_query = request.GET.get('publication', '')
    selected_tag = request.GET.get('tag', '')
    sort_by = request.GET.get('sort_by', 'timestamp')

    posts = Blogs.objects.all()

    if search_query:
        posts = posts.filter(title__icontains=search_query)

    if selected_tag:
        posts = posts.filter(tags__name=selected_tag)

    if sort_by == 'views':
        posts = posts.order_by('-views')
    elif sort_by == 'likes':
        posts = posts.order_by('-likes')
    else:
        posts = posts.order_by('-timeStamp')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()

    return render(request, 'handleblog.html', {
        'page_obj': page_obj, 
        'tags': tags, 
        'sort_by': sort_by,
        'selected_tag': selected_tag
    })

# Vue de détail d'une publication
def post_detail(request, post_id):
    post = get_object_or_404(Blogs, id=post_id)

    if not request.session.get(f'has_seen_post_{post.id}', False):
        post.views += 1
        post.save()
        request.session[f'has_seen_post_{post.id}'] = True

    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = post.liked_by.filter(id=request.user.id).exists()

    if request.method == 'POST' and 'like' in request.POST:
        if request.user.is_authenticated:
            if not user_has_liked:
                post.likes += 1
                post.liked_by.add(request.user)
            else:
                post.likes -= 1
                post.liked_by.remove(request.user)
            post.save()
            return redirect('detail', post_id=post.id)
        else:
            return redirect('login')

    comments = post.comments.filter(parent_comment__isnull=True)
    num_comments = post.comments.count()
    related_posts = Blogs.objects.filter(category=post.category).exclude(id=post.id)[:4]

    return render(request, 'detail.html', {
        'post': post,
        'comments': comments,
        'num_comments': num_comments,
        'related_posts': related_posts,
        'user_has_liked': user_has_liked,
    })

# Vue de recherche
def search(request):
    query = request.GET.get("publication", "")
    liste_publication = Blogs.objects.filter(title__icontains=query)
    return render(request, "search.html", {"liste_publication": liste_publication})

# Vue 'À propos'
def about(request, *args, **kwargs):
    about_obj = About.objects.get(id=1)
    return render(request, 'about.html', {'about': about_obj})

# Vue pour ajouter un commentaire
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Blogs, id=pk)
    if request.method == 'POST':
        comment_body = request.POST.get('comment_body')
        if comment_body:
            parent_obj = None
            parent_id = request.POST.get('parent')
            if parent_id:
                try:
                    parent_obj = Comment.objects.get(id=int(parent_id))
                except (ValueError, Comment.DoesNotExist):
                    parent_obj = None
            
            commenter_name = request.user.get_full_name() or request.user.username

            Comment.objects.create(
                commenter_name=commenter_name,
                comment_body=comment_body,
                post=post,
                user=request.user,
                parent_comment=parent_obj
            )

    return redirect('detail', post_id=pk)

# Vue pour liker un commentaire
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.liked_by.all():
        comment.likes -= 1
        comment.liked_by.remove(user)
    else:
        comment.likes += 1
        comment.liked_by.add(user)
    
    comment.save()
    return redirect('detail', post_id=comment.post.id)

# Vue pour supprimer un commentaire
@login_required
def delete_comment(request, comment_id):
    commentaire = get_object_or_404(Comment, id=comment_id)
    if request.user.username == commentaire.commenter_name or request.user.get_full_name() == commentaire.commenter_name:
        commentaire.delete()
    return redirect(request.META.get('HTTP_REFERER', 'blog'))

# Vue pour la page de contact
def contact(request):
    if request.method == "POST":
        fname = request.POST.get('name')
        femail = request.POST.get('email')
        fphoneno = request.POST.get('num')
        fdesc = request.POST.get('desc')
        if fname and femail and fdesc:
            Contact.objects.create(name=fname, email=femail, phonenumber=fphoneno, description=fdesc)
            messages.success(request, "Merci de nous avoir contactés. Nous vous répondrons bientôt !")
            return redirect('/contact')
    return render(request, 'contact.html')

# Vue pour envoyer un email (alternative)
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            email_message = f"Nom: {name}\nEmail: {email}\nTéléphone: {phone}\n\nMessage:\n{message}"
            email_msg = EmailMessage(
                subject=f'Contact de {name}',
                body=email_message,
                #from_email='chadrackmbupioka@gmail.com',
                to=['chadrackmbujess@gmail.com'],
                headers={'Reply-To': email}
            )
            email_msg.send()
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contacts.html', {'form': form})

# Vue de détail (simplifiée, car déjà gérée par post_detail)
def detail(request, id_publication):
    post = get_object_or_404(Blogs, id=id_publication)
    related_posts = Blogs.objects.filter(category=post.category).exclude(id=id_publication)[:5]
    comments = post.comments.filter(parent_comment__isnull=True)
    num_comments = post.comments.count()
    return render(request, 'detail.html', {
        'post': post,
        'comments': comments,
        'num_comments': num_comments,
        'related_posts': related_posts
    })

# Vue pour la discussion (API)
@login_required
def discussion_view(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        sender_name = request.user.get_full_name() or request.user.username

        if message:
            Discussion.objects.create(post=post, sender=sender_name, message=message)
            return JsonResponse({'status': 'success', 'message': 'Message envoyé !'})
        return JsonResponse({'status': 'error', 'message': 'Message vide.'})

    discussions = post.discussions.all().order_by('timestamp')
    return JsonResponse({'messages': list(discussions.values('sender', 'message', 'timestamp'))})

# Vue pour la liste des commentaires (non utilisée dans le flux principal)
def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comment_list.html', {'comments': comments})

# Vue pour liker un post (non utilisée dans le flux principal)
def like_post(request, post_id):
    post = get_object_or_404(Blogs, id=post_id)
    post.likes += 1
    post.save()
    return redirect('detail', post_id=post.id)
