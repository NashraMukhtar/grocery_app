from rest_framework import serializers
from .models import GroceryItem, RecipeCategory, Recipe, Ingredient, RecipeIngredient, ShoppingItem


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class GroceryItemSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = GroceryItem
        fields = ['id','ingredient']
    
    def create(self, validated_data):
        # Extract the ingredient from validated_data
        request = self.context.get('request')
        ingredient = validated_data.pop('ingredient')
        grocery_item = GroceryItem.objects.create(user=request.user, ingredient=ingredient)
        return grocery_item

    # Custom update method to handle nested Ingredient update
    def update(self, instance, validated_data):
        # Ensure that the ingredient is handled properly on update
        ingredient_data = validated_data.get('ingredient')
        
        # Update the GroceryItem instance's ingredient
        instance.ingredient = Ingredient.objects.get(name=ingredient_data)
        instance.save()

        return instance

class ShoppingItemSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = ShoppingItem
        fields = ['id', 'ingredient']

    def create(self, validated_data):
        user = self.context['request'].user
        ingredient = validated_data.pop('ingredient')
        shopping_item = ShoppingItem.objects.create(user=user, ingredient=ingredient)
        return shopping_item

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient']

class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'category', 'steps', 'recipe_ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', [])
        # Automatically set the 'created_by' field to the logged-in user
        recipe = Recipe.objects.create(created_by=self.context['request'].user, **validated_data)

        recipe_ingredient_objs = []
        for ingredient_data in ingredients_data:
            ingredient = ingredient_data['ingredient']
            recipe_ingredient_objs.append(RecipeIngredient(ingredient=ingredient, recipe=recipe))

        RecipeIngredient.objects.bulk_create(recipe_ingredient_objs)

        return recipe
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', [])

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.steps = validated_data.get('steps', instance.steps)
        instance.save()

        recipe_ingredient_objs = []
        for ingredient_data in ingredients_data:
            ingredient = ingredient_data['ingredient']
            recipe_ingredient_objs.append(RecipeIngredient(ingredient=ingredient, recipe=instance))

        instance.recipe_ingredients.set(recipe_ingredient_objs, bulk=False)

        return instance