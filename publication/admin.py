from django.contrib import admin
from django.db import models
from django import forms
from .models import *
from tinymce.widgets import TinyMCE

# --- Admin Site Configuration ---
#admin.site.site_header = "Administration FADN"
#admin.site.site_title = "Portail d'administration FADN"
#admin.site.index_title = "Bienvenue sur le portail d'administration FADN"

# --- Custom Admin Form for About ---
class AboutAdminForm(forms.ModelForm):
    about_body = forms.CharField(widget=TinyMCE())
    sub_about_body = forms.CharField(widget=TinyMCE())

    class Meta:
        model = About
        fields = '__all__'

# --- Admin Model Classes ---
class AboutAdmin(admin.ModelAdmin):
    form = AboutAdminForm

class ContactAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'authname', 'timeStamp', 'views', 'likes', 'media_type')
    search_fields = ('title', 'authname')
    list_filter = ('media_type', 'category', 'tags')
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            'assets/js/admin_custom.js', # Chemin corrigé
        )

# --- Registering Models with Admin ---
admin.site.register(Contact, ContactAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(About, AboutAdmin)
admin.site.register(Notification)
