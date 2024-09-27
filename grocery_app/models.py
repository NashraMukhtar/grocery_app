from django.db import models
from django.contrib.auth.models import User

class RecipeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', related_name='recipe_ingredients', on_delete=models.CASCADE)
    # quantity = models.CharField(max_length=100, blank=True)  # Optional field for quantity in the recipe

    def __str__(self):
        return f"{self.ingredient.name} for {self.recipe.name}"
    
class GroceryItem(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.ingredient.name}"

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True, related_name='recipes')
    steps = models.TextField()

    def __str__(self):
        return self.name
