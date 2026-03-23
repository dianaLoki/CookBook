from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """Профиль внутри страницы пользователя"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'


class CustomUserAdmin(UserAdmin):
    """Расширенная админка для пользователей с профилем"""
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_recipes_count']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    get_recipes_count.short_description = 'Рецептов'


# Переопределяем стандартную админку пользователя
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Отдельная админка для профилей (на всякий случай)"""
    list_display = ['user', 'avatar_preview', 'bio']
    list_filter = ['user__is_staff']
    search_fields = ['user__username', 'bio']
    readonly_fields = ['avatar_preview']

    def avatar_preview(self, obj):
        """Показывает миниатюру аватара в админке"""
        if obj.avatar:
            from django.utils.html import format_html
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return 'Нет аватара'

    avatar_preview.short_description = 'Аватар'