from django.contrib import admin
from .models import *

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'authname', 'timeStamp', 'views', 'likes', 'media_type')
    search_fields = ('title', 'authname')
    list_filter = ('media_type', 'category', 'tags')

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            'assets/js/admin_custom.js', # Chemin corrigé
        )

admin.site.register(Contact)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(About)
admin.site.register(Notification)
