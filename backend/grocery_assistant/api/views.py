from functools import partial

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from grocery_assistant.settings import ROLES_PERMISSIONS
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .paginations import StandardResultsSetPagination
from .permissions import IsAuthor, PermissonForRole
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer)


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
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Users_me'))
        ],
        url_path=r'(?P<user_id>[0-9]+)',
        url_name='UserView'
    )
    def user_id(self, request, user_id) -> Response:
        serializer = self.get_serializer(User.objects.get(id=user_id))
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get('Recipe')),
        IsAuthor,
    )
    pagination_class = StandardResultsSetPagination

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Recipe'))
        ],  # только get
        url_path='download_shopping_cart'
    )
    def get_shopping_cart(self, request):
        return HttpResponse('Это был GET-запрос!')

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
