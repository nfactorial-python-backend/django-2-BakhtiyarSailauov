from django.contrib import admin
from .models import News, Comments


class CommentInline(admin.TabularInline):
    model = Comments
    extra = 5


class AdminNews(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ["title", "content", "created_at", "has_comments"]


admin.site.register(News, AdminNews)
