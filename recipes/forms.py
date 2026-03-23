from .models import Recipe, Comment, Rating
from django import forms


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'steps', 'duration', 'servings', 'complexity', 'category', 'image']
        labels = {'name': 'Название',
                  'description': 'Описание',
                  'ingredients': 'Ингредиенты',
                  'steps': 'Шаги приготовления',
                  'duration': 'Длительность приготовления',
                  'servings': 'Кол-во порций',
                  'complexity': 'Сложность выполнения',
                  'category': 'Категория рецепта',
                  'image': 'Фото рецепта'}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Ваш комментарий'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш комментарий...'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        labels = {
            'rating': 'Оценка'
        }
        widgets = {
            'rating': forms.RadioSelect
        }