from django.urls import path
from publication import views  # Importation des vues du fichier 'views.py'
from django.urls import reverse  # Importation de 'reverse' pour générer des URLs

urlpatterns = [
    # URL pour la page d'accueil
    path('', views.home, name='home'),

    # URL pour la page "À propos"
    path('about', views.about, name='about'),

    # URL pour la page de contact
    path('contact', views.contact, name='contact'),

    # URL pour afficher la liste des blogs
    path('blog', views.handleblog, name='blog'),

    # URL pour ajouter un commentaire à un post
    path('commentaire/<int:pk>/add-comment', views.add_comment, name='add-comment'),

    # URL pour liker un commentaire
    path('like-comment/<int:comment_id>/', views.like_comment, name='like-comment'),

    # URL pour afficher la liste des commentaires
    path('comments', views.comment_list, name='comment_list'),

    # URL pour supprimer un commentaire
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),

    # URL pour afficher les détails d'un post
    path('detail/<int:post_id>/', views.post_detail, name='detail'),

    # URL pour la recherche dans les blogs
    path('search/', views.handleblog, name='search'),

    # URL pour liker un post
    path('like/<int:post_id>/', views.like_post, name='like-post'),
    path('discussion/<int:pk>/', views.discussion_view, name='discussion'),


]
