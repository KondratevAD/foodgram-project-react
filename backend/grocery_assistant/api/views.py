from functools import partial

from django.shortcuts import get_object_or_404
from grocery_assistant.settings import ROLES_PERMISSIONS
from recipes.models import Favorite, Follow, Ingredient, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from users.models import User

from .filePDF import get_pdf
from .filters import IngredientFilter, RecipeFilter
from .paginations import StandardResultsSetPagination
from .permissions import IsAuthor, PermissonForRole
from .serializers import (FavoriteSerializer, FolllowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get('Users')),
    )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Users_me'))
        ],
        url_path='me'
    )
    def user_me(self, request) -> Response:
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Users_id'))
        ],
        url_path=r'(?P<user_id>[0-9]+)',
    )
    def user_id(self, request, user_id) -> Response:
        serializer = self.get_serializer(User.objects.get(id=user_id))
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Users_me'))
        ],
        url_path='subscriptions',
    )
    def user_favorite(self, request) -> Response:
        author_list = set()
        for _ in Follow.objects.filter(
                user_id=request.user.id
        ).select_related('author'):
            author_list.add(_.author)
        data = self.filter_queryset(User.objects.filter(
            id__in=[i.id for i in author_list]).all())
        page = self.paginate_queryset(data)
        serializer = FolllowSerializer(page, context=request, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, {'filter': filter})


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get('Tags')),
    )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get('Ingredients')),
    )
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get('Recipe')),
        IsAuthor,
    )
    pagination_class = StandardResultsSetPagination
    filterset_class = RecipeFilter

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Shopping_cart'))
        ],
        url_path='download_shopping_cart'
    )
    def get_shopping_cart(self, request):
        data = dict()
        recipes = Recipe.objects.filter(
            favorite__user=self.request.user,
            favorite__shopping_cart=True
        ).prefetch_related('ingredients')
        if not recipes:
            raise ParseError(
                detail={
                    'error': ['Your shopping list is empty.']
                }
            )
        for recipe in recipes:
            ingredients = [
                ingredients for ingredients in recipe.ingredients.all()
            ]
            for ingredient in ingredients:
                if f'{ingredient.ingredient.id}' in data:
                    data[
                        f'{ingredient.ingredient.id}'
                    ]['amount'] += ingredient.amount
                else:
                    data.update(
                        {
                            f'{ingredient.ingredient.id}': {
                                'name': ingredient.ingredient.name,
                                'measurement_unit':
                                    ingredient.ingredient.measurement_unit,
                                'amount': ingredient.amount
                            }
                        }
                    )
        data = dict(sorted(data.items(), key=lambda item: item[1]['name']))
        return get_pdf(data)

    def perform_create(self, serializer):
        if 'tags' not in self.request.data:
            raise ParseError(detail={'tags': ['This field is required.']})
        tag_id = self.request.data['tags']
        if type(tag_id) is not list:
            raise ParseError(detail={'tags': ['This field should be a list.']})
        author = self.request.user
        serializer.save(author=author, tags=tag_id)

    def perform_update(self, serializer):
        if 'tags' not in self.request.data:
            raise ParseError(detail={'tags': ['This field is required.']})
        tag_id = self.request.data['tags']
        if type(tag_id) is not list:
            raise ParseError(detail={'tags': ['This field should be a list.']})
        serializer.save(tags=tag_id)

    def perform_destroy(self, instance):
        instance.ingredients.all().delete()
        instance.delete()


@api_view(['GET', 'DELETE'])
def shopping_cart(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'GET':
        favor = Favorite.objects.get_or_create(
            recipe_id=id,
            user_id=request.user.id
        )[0]
        if favor.shopping_cart is True:
            raise ParseError(
                detail={
                    'tags': ['The recipe is already on your shopping list.']
                }
            )
        else:
            favor.shopping_cart = True
            favor.save()
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data)
    else:
        favor = Favorite.objects.get(recipe_id=id, user_id=request.user.id)
        if favor.shopping_cart is False:
            raise ParseError(
                detail={
                    'tags': ['The recipe is not on your shopping list.']
                }
            )
        else:
            favor.shopping_cart = False
            favor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
def favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'GET':
        favor = Favorite.objects.get_or_create(
            recipe_id=id,
            user_id=request.user.id
        )[0]
        if favor.favorite is True:
            raise ParseError(
                detail={
                    'tags': [
                        'The recipe is already on your shopping list.']
                }
            )
        else:
            favor.favorite = True
            favor.save()
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data)
    else:
        favor = Favorite.objects.get(recipe_id=id, user_id=request.user.id)
        if favor.favorite is False:
            raise ParseError(
                detail={
                    'tags': ['The recipe is not on your favorite list.']
                }
            )
        else:
            favor.favorite = False
            favor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'DELETE'])
def follow(request, id):
    author = get_object_or_404(User, id=id)
    if author.id == request.user.id:
        raise ParseError(
            detail={
                'error': [
                    "You can't subscribe/unsubscribe to yourself"]
            }
        )
    if request.method == 'GET':
        follow, stat = Follow.objects.get_or_create(
            author_id=author.id,
            user_id=request.user.id
        )
        if stat is False:
            raise ParseError(
                detail={
                    'error': [
                        'You are already subscribed to this user.']
                }
            )
        serializer = FolllowSerializer(author, context=request)
        return Response(serializer.data)
    else:
        follow = Follow.objects.filter(
            user_id=request.user.id,
            author_id=author.id
        )
        if follow:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ParseError(
                detail={
                    'tags': ['You are not subscribed to this user.']
                }
            )
