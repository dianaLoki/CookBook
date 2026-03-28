from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search'),  # ← первым
    path('favorites', views.FavoritesListView.as_view(), name='favorites'),
    path('recipe/<int:recipe_id>/', views.DetailRecipeView.as_view(), name='recipe_detail'),
    path('category/<int:category_id>/', views.recipe_by_category, name='recipe_by_category'),
    path('add_recipe', views.AddRecipe.as_view(), name='add_recipe'),
    path('recipe_list', views.RecipesListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/edit/', views.UpdateRecipeView.as_view(), name='recipe_edit'),
    path('recipe/<int:pk>/delete/', views.DeleteRecipeView.as_view(), name='recipe_delete'),
    path('recipe/<int:recipe_id>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('recipe/<int:recipe_id>/rate/', views.RateRecipeView.as_view(), name='rate_recipe'),
    path('recipe/<int:recipe_id>/favorite/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('comment/<int:comment_id>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
]