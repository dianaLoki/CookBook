from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe, Category, Comment, Rating


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'status', 'date']
    list_filter = ['status', 'author']
    search_fields = ['name', 'author__username']
    actions = ['approve_recipes', 'reject_recipes']

    def approve_recipes(self, request, queryset):
        queryset.update(status='published')

    approve_recipes.short_description = "Опубликовать выбранные рецепты"

    def reject_recipes(self, request, queryset):
        queryset.update(status='rejected')

    reject_recipes.short_description = "Отклонить выбранные рецепты"


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