from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect


class About(models.Model):
    title = models.CharField(max_length=500)
    about_body = models.TextField()  # Remplacer TextField par FroalaField
    sub_about_body = models.TextField()  # Remplacer TextField par FroalaField
    image1_about = models.ImageField(upload_to='image_about')
    image2_about = models.ImageField(upload_to='image_about')
    cree = models.TextField(default='Date de création')
    site_web = models.TextField(default='Site web')
    contact = models.TextField(default='Contact')
    pays = models.TextField(default='Pays')
    ville = models.TextField(default='Ville')
    but = models.TextField(default='But')
    email = models.TextField(default='E-mail')
    statut = models.TextField(default='Statut')

    class Meta:
        verbose_name = ("A propos")

    def __str__(self):
        return self.title

# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=10)
    description = models.TextField()  # Utilisation de FroalaField pour un éditeur de texte riche

    def __str__(self):
        return self.name
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name = ("Catégorie")
        verbose_name_plural = ("Catégories")

    def __str__(self):
        return self.name

class Blogs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    img = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
    ]
    media_type = models.CharField(
        max_length=5,
        choices=MEDIA_CHOICES,
        default='image',
    )
    timeStamp = models.DateTimeField(auto_now_add=True)
    authname = models.CharField(max_length=100,default="Andy-Disu")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='publications', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

    # Relation ManyToMany pour les likes
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        verbose_name = ("Publication")
        verbose_name_plural = ("Publications")

    def __str__(self):
        return self.title

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Un utilisateur peut liker un post une seule fois


class Comment(models.Model):
    commenter_name = models.CharField(max_length=100)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Blogs', related_name='comments', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.commenter_name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisateur qui recevra la notification
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    related_comment = models.ForeignKey('Comment', null=True, blank=True, on_delete=models.SET_NULL)  # Commentaire lié

    def __str__(self):
        return f'{self.user.username} - {self.message}'

class Discussion(models.Model):
    post = models.ForeignKey('Blogs', on_delete=models.CASCADE, related_name='discussions')
    sender = models.CharField(max_length=100)  # Le nom de l'utilisateur qui envoie le message
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.message[:20]}'



class DiscussionMessage(models.Model):
    post = models.ForeignKey('Blogs', related_name='discussion_messages', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.author} sur {self.post.title}"
