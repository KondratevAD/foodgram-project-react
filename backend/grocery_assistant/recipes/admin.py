from django.contrib import admin
from users.models import User

from .models import Favorite, Follow, Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного"""
    list_display = (
        'pk',
        'user',
        'recipe',
        'shopping_cart',
        'favorite'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка полльзователей"""
    list_display = (
        'pk',
        'username',
        'email',
        'role'
    )
    list_filter = ('email', 'username')

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка подписчиков"""
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
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = ('ingredient',)
    list_filter = ('ingredient',)
