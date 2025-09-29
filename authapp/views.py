from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Profile

def signup(request):
    if request.method == "POST":
        get_first_name = request.POST.get('first_name')
        get_last_name = request.POST.get('last_name')
        get_email = request.POST.get('email')
        get_password = request.POST.get('pass1')
        get_confirm_password = request.POST.get('pass2')

        if get_password != get_confirm_password:
            messages.info(request, "Les mots de passe ne correspondent pas.")
            return redirect('signup')

        if User.objects.filter(username=get_email).exists():
            messages.warning(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('signup')

        myuser = User.objects.create_user(get_email, get_email, get_password)
        myuser.first_name = get_first_name
        myuser.last_name = get_last_name
        myuser.save()

        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            profile = Profile.objects.create(user=myuser, profile_picture=fs.url(filename))
            profile.save()

        login(request, myuser)
        messages.success(request, "Utilisateur enregistré avec succès")
        return redirect('/')

    return render(request, 'signup.html')

def handleLogin(request):
    if request.method == "POST":
        get_email = request.POST.get('name')
        get_password = request.POST.get('pass1')
        next_page = request.POST.get('next', '/')

        myuser = authenticate(username=get_email, password=get_password)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Connexion réussie")
            return redirect(next_page)
        else:
            messages.error(request, "Informations d'identification non valides")
            # En cas d'échec, on recharge la page de connexion en passant 'next'
            return render(request, 'login.html', {'next': next_page})
    
    # Pour une requête GET, on affiche le formulaire
    next_page = request.GET.get('next', '/')
    return render(request, 'login.html', {'next': next_page})

def handleLogout(request):
    logout(request)
    messages.success(request, 'Déconnexion avec succès')
    # Toujours rediriger vers la page de connexion après la déconnexion
    return redirect('login')
