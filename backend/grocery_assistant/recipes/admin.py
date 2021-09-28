from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов"""
    list_display = (
        'pk',
        'name',
        'text',
        'author',
        'image',
        'coking_time',
        'pub_date'
    )
    search_fields = ('name',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


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
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов"""
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов рецепта"""
    list_display = (
        'pk',
        'ingredient',
        'amount'
    )
    search_fields = ('ingredient',)
    list_filter = ('amount',)
    empty_value_display = '-пусто-'
