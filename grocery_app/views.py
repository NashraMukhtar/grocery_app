from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes  
from rest_framework import generics, status
from core.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import GroceryItem, RecipeCategory, Recipe, RecipeIngredient, Ingredient, ShoppingItem
from .serializers import GroceryItemSerializer, RecipeCategorySerializer, RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer, ShoppingItemSerializer


# List and Create Grocery Items for the authenticated user
class GroceryItemListCreateView(generics.ListCreateAPIView):
    queryset = GroceryItem.objects.all()
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryItem.objects.filter(user=self.request.user)

# Retrieve, Update, and Delete Grocery Items
class GroceryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryItem.objects.filter(user=self.request.user)
    

class ShoppingItemListCreateView(generics.ListCreateAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShoppingItem.objects.filter(user=self.request.user)

class ShoppingItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return items that belong to the logged-in user
        return ShoppingItem.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # Custom behavior for deletion, if needed (e.g., notifying the user)
        instance.delete()
        return Response({"message": "Shopping item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# List and Create Recipe Inrgedients
class RecipeIngredientListCreateView(generics.ListCreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecipeIngredient.objects.all()

# Retrieve, Update, and Delete Grocery Items
class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeIngredientSerializer

    def get_queryset(self):
        return RecipeIngredient.objects.all()
    


# List and Create Ingredients
class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]

    def get_queryset(self):
        return Ingredient.objects.all()

# Retrieve, Update, and Delete Ingredients
class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]

    def get_queryset(self):
        return Ingredient.objects.all()



# List all Recipe Categories and Create a new Recipe Category
class RecipeCategoryListCreateView(generics.ListCreateAPIView):
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer

    def get_queryset(self):
        return RecipeCategory.objects.all()

# Retrieve, Update, and Delete Recipe Category by ID
class RecipeCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeCategorySerializer

    def get_queryset(self):
        return RecipeCategory.objects.all()



# List all Recipes and Create a new Recipe
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Recipe.objects.all()

# Retrieve, Update, and Delete Recipe by ID
class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Recipe.objects.all()

class UserRecipeListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)



@api_view(['GET'])
def suggest_recipes(request):
    # Get grocery items for the authenticated user and convert ingredient names to lowercase for consistent comparison
    grocery_items = GroceryItem.objects.filter(user=request.user).values_list('ingredient__name', flat=True)
    grocery_items = [item.lower() for item in grocery_items]

    # Get all recipes
    recipes = Recipe.objects.all()

    # List to store recipe suggestions with ingredient match counts
    suggested_recipes = []

    for recipe in recipes:
        # Get recipe ingredients through the RecipeIngredient model
        recipe_ingredients = recipe.recipe_ingredients.values_list('ingredient__name', flat=True)
        recipe_ingredients = [ingredient.lower() for ingredient in recipe_ingredients]

        # Find matching ingredients between recipe and grocery items
        matched_ingredients = set(recipe_ingredients).intersection(grocery_items)
        unmatched_ingredients = set(recipe_ingredients).difference(grocery_items)

        # Create a data structure to hold the recipe and its match count
        suggested_recipes.append({
            'recipe': recipe,
            'match_count': len(matched_ingredients),
            'matched_ingredients': matched_ingredients,
            'unmatched_ingredients': unmatched_ingredients
        })

    # Sort recipes by match_count in descending order (most matching first)
    suggested_recipes = sorted(suggested_recipes, key=lambda x: x['match_count'], reverse=True)

    # Custom response structure for matched and unmatched ingredients
    response_data = []
    for suggestion in suggested_recipes:
        recipe_data = RecipeSerializer(suggestion['recipe']).data
        recipe_data['matched_ingredients'] = list(suggestion['matched_ingredients'])
        recipe_data['unmatched_ingredients'] = [{'name': ing, 'highlight': 'red'} for ing in suggestion['unmatched_ingredients']]
        response_data.append(recipe_data)

    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def move_to_grocery_list(request, pk):
    try:
        shopping_item = ShoppingItem.objects.get(pk=pk, user=request.user)
    except ShoppingItem.DoesNotExist:
        return Response({"error": "Shopping item not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if the GroceryItem already exists for the user
    if GroceryItem.objects.filter(ingredient=shopping_item.ingredient, user=request.user).exists():
        return Response({"error": "Item already exists in your grocery list."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new GroceryItem
    GroceryItem.objects.create(user=request.user, ingredient=shopping_item.ingredient)

    # Delete the ShoppingItem after moving
    shopping_item.delete()

    return Response({"success": "Item moved to grocery list."}, status=status.HTTP_200_OK)



