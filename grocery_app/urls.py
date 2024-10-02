from django.urls import path
from .views import GroceryItemListCreateView, GroceryItemDetailView, RecipeCategoryListCreateView, RecipeCategoryDetailView, RecipeListCreateView, RecipeDetailView, suggest_recipes, IngredientListCreateView, IngredientDetailView, RecipeIngredientListCreateView, RecipeIngredientDetailView, ShoppingItemListCreateView, move_to_grocery_list, ShoppingItemDetailView, UserRecipeListView

urlpatterns = [
    path('grocery-items/', GroceryItemListCreateView.as_view(), name='grocery-list-create'),
    path('grocery-items/<int:pk>/', GroceryItemDetailView.as_view(), name='grocery-detail-update-delete'),

    path('shopping-items/', ShoppingItemListCreateView.as_view(), name='shopping-items'),
    path('shopping-item/<int:pk>/', ShoppingItemDetailView.as_view(), name='shopping-item-detail'),
    path('shopping-item/<int:pk>/move-to-grocery/', move_to_grocery_list, name='move-to-grocery'),

    path('recipe-ingredients/', RecipeIngredientListCreateView.as_view(), name='recipeingredients-list-create'),
    path('recipe-ingredients/<int:pk>/', RecipeIngredientDetailView.as_view(), name='recipeingredients-detail-update-delete'),

    path('categories/', RecipeCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', RecipeCategoryDetailView.as_view(), name='category-detail-update-delete'),

    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail-update-delete'),

    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail-update-delete'),
    path('my-recipes/', UserRecipeListView.as_view(), name='user-recipes'),

    path('suggest-recipes/', suggest_recipes, name='suggest-recipes'),
]
