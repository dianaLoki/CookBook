from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'

    def __str__(self):
        return self.name

class Recipe(models.Model):
    COMPLEXITY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    steps = models.TextField()
    ingredients = models.TextField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Время в минутах")
    servings = models.PositiveIntegerField(
        default=1,
        help_text="Количество порций"
    )
    complexity = models.CharField(
        max_length=10,
        choices=COMPLEXITY_CHOICES,
        default='medium'
    )
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='recipes', null=True, default=None
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    image = models.ImageField(
        upload_to='recipes/img/%Y/%m/%d/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        db_table = 'cooking_recipes'
        ordering = ['-date']


    def __str__(self):
        return self.name


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               null=False,
                               blank=False,
                               related_name='comments'
                               )
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             related_name='comments'
                             )
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.recipe.name}'

    class Meta:
        ordering = ['-date']

class Rating(models.Model):
    RATING_CHOICE = [
        ('1', 'Ужасно'),
        ('2', 'Плохо'),
        ('3', 'Нормально'),
        ('4', 'Хорошо'),
        ('5', 'Отлично')
    ]
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               null=False,
                               blank=False,
                               related_name='ratings'
                               )
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             related_name='ratings'
                             )
    rating = models.IntegerField(choices=RATING_CHOICE, default=5)

    def __str__(self):
        return f'{self.user.username} оценил {self.recipe.name} на {self.rating}'

    class Meta:
        unique_together = ['recipe', 'user']
        ordering = ['-rating']


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(),
        on_delete=models.CASCADE,
        related_name='favorites', null=True, default=None
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL,
                               related_name='favorited_by',
                               null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'recipe']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.recipe.name}'