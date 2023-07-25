from django.contrib import admin
from .models import Post,Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'date_posted','comment_body') 
    
admin.site.register(Post)

admin.site.register(Comment)
