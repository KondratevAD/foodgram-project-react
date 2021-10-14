import django_filters
from django_filters.rest_framework import filters
from recipes.models import Ingredient, Recipe
from users.models import User


class RecipeFilter(django_filters.FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorite__favorite',
        method='filter_favorite'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='favorite__shopping_cart',
        method='filter_favorite'
    )

    def filter_favorite(self, queryset, name, value):
        if value is False:
            return queryset.exclude(**{name: True}).all()
        return queryset.filter(**{name: True}).all()

    class Meta:
        model = Recipe
        fields = ['author', 'tags']


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name']
