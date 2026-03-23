from django.contrib import admin
from .models import Recipe, Category, Comment, Rating


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'author', 'duration', 'complexity', 'date', 'servings']
    search_fields = ['name', 'description', 'author__username']
    list_filter = ['category', 'author', 'complexity', 'date', 'duration']
    list_display_links = ['name']
    readonly_fields = ['date']
    actions = ['make_published', 'reset_views']

    def make_published(self, request, queryset):
        queryset.update(status='published')

    make_published.short_description = "Опубликовать выбранные рецепты"

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