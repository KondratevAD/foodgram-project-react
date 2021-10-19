from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.validators import UniqueTogetherValidator
from users.models import User
from util.Image_base64 import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {'password': {'write_only': True}}
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        model = User

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def get_is_subscribed(self, obj):
        return obj.follower.values('author_id').filter(
            author_id=self.context['request'].user.id
        ).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )
        model = Tag
        extra_kwargs = {'color': {'required': True}}


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )
        model = RecipeIngredient

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe
        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=['id'],
                message='Вы уже добавили этот ингредиент'
            )
        ]

    def create(self, validated_data):
        recipe = Recipe.objects.create(
            name=validated_data['name'],
            author=validated_data['author'],
            text=validated_data['text'],
            image=validated_data['image'],
            cooking_time=validated_data['cooking_time']
        )
        for tag_id in validated_data['tags']:
            if type(tag_id) is not int:
                recipe.delete()
                raise ParseError(
                    detail={'tags': ['A valid integer is required.']}
                )
            tag = get_object_or_404(Tag, id=tag_id)
            recipe.tags.add(tag)
        for ingredient in self.initial_data['ingredients']:
            ingredient_mod = Ingredient.objects.get(id=ingredient['id'])
            recipe_ingredient = RecipeIngredient.objects.create(
                ingredient=ingredient_mod,
                amount=ingredient['amount']
            )
            recipe.ingredients.add(recipe_ingredient)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        for tag_id in validated_data['tags']:
            if type(tag_id) is not int:
                raise ParseError(
                    detail={'tags': ['A valid integer is required.']}
                )
            tag = get_object_or_404(Tag, id=tag_id)
            instance.tags.clear()
            instance.tags.add(tag)
        instance.ingredients.all().delete()
        for ingredient in self.initial_data['ingredients']:
            ingredient_mod = get_object_or_404(Ingredient, id=ingredient['id'])
            recipe_ingredient = RecipeIngredient.objects.create(
                ingredient=ingredient_mod,
                amount=ingredient['amount']
            )
            instance.ingredients.add(recipe_ingredient)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            favor = Favorite.objects.filter(
                recipe_id=obj.id,
                user_id=self.context['request'].user.id
            ).first()
            if favor:
                return favor.favorite
            return False
        return False

    def get_is_in_shopping_cart(self, obj):
        favorite = Favorite.objects.filter(
            recipe_id=obj.id,
            user_id=self.context['request'].user.id
        )
        if self.context['request'].user.is_authenticated and favorite:
            return favorite[0].shopping_cart
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipe


class FolllowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = User

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            author_id=obj.id,
            user_id=self.context.user.id
        ).exists()

    def get_recipes(self, obj):
        if 'recipes_limit' in self.context.GET:
            count = int(self.context.GET['recipes_limit'])
            data = Recipe.objects.filter(author_id=obj.id).all()[:count]
        else:
            data = Recipe.objects.filter(author_id=obj.id).all()
        serializers = FavoriteSerializer(data, many=True)
        return serializers.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author_id=obj.id).count()
