from functools import partial

from grocery_assistant.settings import ROLES_PERMISSIONS
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .paginations import StandardResultsSetPagination
from .permissions import PermissonForRole
from .serializers import (IngredientSerializer, RecipeSerializer,
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
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Users_me'))
        ],
        url_path=r'(?P<user_id>[0-9]+)',
        url_name='UserView'
    )
    def user_id(self, request, user_id) -> Response:
        print('-----------------------------------------------')
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
    )
    pagination_class = StandardResultsSetPagination
