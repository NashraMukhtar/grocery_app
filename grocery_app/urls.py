from django.urls import path
from .views import GroceryItemListCreateView, GroceryItemDetailView, RecipeCategoryListCreateView, RecipeCategoryDetailView, RecipeListCreateView, RecipeDetailView, suggest_recipes, IngredientListCreateView, IngredientDetailView, RecipeIngredientListCreateView, RecipeIngredientDetailView

urlpatterns = [
    path('grocery-items/', GroceryItemListCreateView.as_view(), name='grocery-list-create'),
    path('grocery-items/<int:pk>/', GroceryItemDetailView.as_view(), name='grocery-detail-update-delete'),

    path('recipe-ingredients/', RecipeIngredientListCreateView.as_view(), name='recipeingredients-list-create'),
    path('recipe-ingredients/<int:pk>/', RecipeIngredientDetailView.as_view(), name='recipeingredients-detail-update-delete'),

    path('categories/', RecipeCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', RecipeCategoryDetailView.as_view(), name='category-detail-update-delete'),

    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail-update-delete'),

    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail-update-delete'),

    path('suggest-recipes/', suggest_recipes, name='suggest-recipes'),
]
