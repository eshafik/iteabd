from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish', 'post_status')
    list_filter = ('post_status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    date_hierarchy = 'publish'
