from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe, Category, Comment, Rating


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'author', 'duration', 'image_preview', 'date']
    search_fields = ['name', 'description', 'author__username']
    list_filter = ['category', 'author', 'complexity', 'date', 'duration']
    list_display_links = ['name']
    readonly_fields = ['date']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 8px;" />', obj.image.url)
        return 'Нет фото'

    image_preview.short_description = 'Фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'date']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'date', 'is_active']
    list_filter = ['is_active', 'date']
    search_fields = ['text', 'user__username']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe', 'rating']
    list_filter = ['rating']
    search_fields = ['user__username', 'recipe__name']