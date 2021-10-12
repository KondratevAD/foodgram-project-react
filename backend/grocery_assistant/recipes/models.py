from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Recipe(models.Model):
    """Рецепт"""
    name = models.CharField(
        'Рецепт',
        max_length=200,
        help_text='Название рецепта'
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Описание рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
        help_text='Изображение'
    )
    ingredients = models.ManyToManyField(
        'RecipeIngredient',
        verbose_name='Ингредиенты',
        help_text='Ингредиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тег',
        help_text='Тег',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
    """Тэг рецепта"""
    name = models.CharField(
        'Тэг',
        max_length=200,
        help_text='Название тега',
        unique=True
    )
    color = ColorField(unique=True)
    slug = models.SlugField(
        'slug',
        max_length=200,
        unique=True,
        help_text='Slug тега'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Ингредиенты"""
    name = models.CharField(
        'Ингредиент',
        max_length=200,
        help_text='Название ингредиента'
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200,
        help_text='Единицы измерения ингредиента'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('id', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    """Ингредиенты рецепта"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент рецепта',
        help_text='Ингредиент рецепта'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Количество ингредиента',
        validators=[MinValueValidator(1)]
    )

    def __str__(self) -> str:
        return self.ingredient.name

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    """Избранное"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite'
    )
    shopping_cart = models.BooleanField(
        verbose_name='Корзина покупок',
        default=False
    )
    favorite = models.BooleanField(
        verbose_name='Избранное',
        default=False
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Follow(models.Model):
    """Подписки"""
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Подписант'
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
