from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddRecipeForm, CommentForm, RatingForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.urls import reverse_lazy, get_urlconf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Recipe, Comment, Rating, Favorite
from django.db.models import Avg, Q
from django.contrib import messages
from functools import reduce
from operator import or_



class IndexView(ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    context_object_name = 'latest_recipes'

    def get_queryset(self):
        return Recipe.objects.all().order_by('-date')[:6]


class DetailRecipeView(DetailView):
    template_name = 'recipes/detail.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object

        context['comments'] = recipe.comments.filter(is_active=True).order_by('-date')[:10]
        avg_rating = recipe.ratings.aggregate(Avg('rating'))['rating__avg']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['ratings_count'] = recipe.ratings.count()

        context['comment_form'] = CommentForm()
        context['rating_form'] = RatingForm()

        if self.request.user.is_authenticated:
            user_rating = recipe.ratings.filter(user=self.request.user).first()
            context['user_rating'] = user_rating.rating if user_rating else None
        else:
            context['user_rating'] = None

        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user,
                recipe=recipe
            ).exists()
        else:
            context['is_favorite'] = False

        return context

    def get_object(self):
        recipe_id = self.kwargs.get('recipe_id')
        return get_object_or_404(Recipe, pk=recipe_id)


def recipe_by_category(request, category_id):
    return render(request, 'recipes/recipe_by_category.html')
    #return HttpResponse(f'Список рецептов с категорией {category_id}')


class AddRecipe(LoginRequiredMixin, CreateView):
    form_class = AddRecipeForm
    template_name = 'recipes/add_recipe.html'
    title_page = 'Добавление рецепта'
    success_url = reverse_lazy('recipes:index')

    def form_valid(self, form):
        w = form.save(commit= False)
        w.author = self.request.user
        return super().form_valid(form)

class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.all().order_by('-date')


class UpdateRecipeView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name', 'description', 'category', 'duration', 'complexity', 'servings', 'ingredients', 'steps', 'image']
    template_name = 'recipes/add_recipe.html'

    def get_success_url(self):
        return reverse_lazy('recipes:recipe_detail', args=[self.object.id])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("Вы не автор этого рецепта")
        return super().dispatch(request, *args, **kwargs)


class DeleteRecipeView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/deleting_recipe_done.html'
    success_url = reverse_lazy('recipes:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied("Вы не автор этого рецепта")
        return super().dispatch(request, *args, **kwargs)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.recipe_id = self.kwargs['recipe_id']
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Комментарий добавлен!')
        return redirect('recipes:recipe_detail', recipe_id=self.kwargs['recipe_id'])

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при добавлении комментария')
        return redirect('recipes:recipe_detail', recipe_id=self.kwargs['recipe_id'])


class RateRecipeView(LoginRequiredMixin, View):
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        rating_value = request.POST.get('rating')

        if rating_value:
            rating, created = Rating.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': rating_value}
            )

            if created:
                messages.success(request, 'Спасибо за оценку!')
            else:
                messages.success(request, 'Оценка обновлена!')
        else:
            messages.error(request, 'Выберите оценку')

        return redirect('recipes:recipe_detail', recipe_id=recipe.id)


class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        favorite = Favorite.objects.filter(user=request.user, recipe=recipe).first()

        if favorite:
            favorite.delete()
            messages.info(request, f'Рецепт "{recipe.name}" удален из избранного')
        else:
            Favorite.objects.create(user=request.user, recipe=recipe)
            messages.success(request, f'Рецепт "{recipe.name}" добавлен в избранное')

        return redirect('recipes:favorites')

class FavoritesListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'recipes/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related(
            'recipe', 'recipe__category', 'recipe__author'
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites_count'] = self.get_queryset().count()
        return context

class SearchResultsView(ListView):
    model = Recipe
    template_name = 'recipes/search_results.html'
    context_object_name = 'recipes'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            variants = [query, query.lower(), query.upper(), query.capitalize()]
            q_list = [Q(name__contains=v) | Q(description__contains=v) for v in set(variants)]
            q_objects = reduce(or_, q_list)
            return Recipe.objects.filter(q_objects).order_by('-date')
        return Recipe.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context