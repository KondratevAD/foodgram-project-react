from django.contrib.auth.hashers import make_password
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import User


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
        # read_only_fields = ['email', 'username', 'first_name', 'last_name' ]

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
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
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

    def get_is_favorited(self, obj):
        return obj.favorite.values('user_id').filter(
            user_id=self.context['request'].user.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.favorite.get(
                user_id=self.context['request'].user.id
            ).shopping_cart
        return False
