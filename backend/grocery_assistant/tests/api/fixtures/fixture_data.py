import tempfile

import pytest


@pytest.fixture
def tag():
    from recipes.models import Tag
    return Tag.objects.create(
        name='Тестовый тэг',
        color='#000000',
        slug='Тестовый слаг'
    )


@pytest.fixture
def ingredient():
    from recipes.models import Ingredient
    return Ingredient.objects.create(
        name='Тестовый ингредиент',
        measurement_unit='шт'
    )


@pytest.fixture
def recipe(user, tag):
    from recipes.models import Recipe
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    recipe = Recipe.objects.create(
        name='Тестовый рецепт 1',
        text='Тестовое описание',
        author=user,
        image=image,
        cooking_time=120
    )
    recipe.tags.add(tag)
    return recipe


@pytest.fixture
def recipe_ingredient(ingredient, recipe):
    from recipes.models import RecipeIngredient
    return RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=120
    )


@pytest.fixture
def another_recipe(another_user, tag):
    from recipes.models import Recipe
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    recipe = Recipe.objects.create(
        name='Тестовый рецепт 2',
        text='Тестовое описание 2',
        author=another_user,
        image=image,
        cooking_time=120
    )
    recipe.tags.add(tag)
    return recipe


@pytest.fixture
def another_recipe_ingredient(ingredient, another_recipe):
    from recipes.models import RecipeIngredient
    return RecipeIngredient.objects.create(
        recipe=another_recipe,
        ingredient=ingredient,
        amount=120
    )
