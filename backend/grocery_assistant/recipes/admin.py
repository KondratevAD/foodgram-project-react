from django.contrib import admin
from users.models import User

from .models import Favorite, Follow, Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
        'shopping_cart',
        'favorite'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role'
    )
    list_filter = ('email', 'username')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов"""
    list_display = (
        'pk',
        'name',
        'text',
        'author',
        'cooking_time',
        'in_favorite'
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')

    @admin.display
    def in_favorite(self, obj):
        return obj.favorite.filter(favorite=True).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка тегов"""
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов"""
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов рецепта"""
    list_display = (
        'pk',
        'ingredient',
        'amount'
    )
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
