import io
from functools import partial

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from grocery_assistant.settings import ROLES_PERMISSIONS
from recipes.models import Favorite, Follow, Ingredient, Recipe, Tag
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

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
            partial(PermissonForRole, ROLES_PERMISSIONS.get('Users_me'))
        ],
        url_path=r'(?P<user_id>[0-9]+)',
    )
    def user_id(self, request, user_id) -> Response:
        serializer = self.get_serializer(User.objects.get(id=user_id))
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,  # нужна пагинация
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
        data = User.objects.filter(
            id__in=[i.id for i in author_list]).all()
        serializer = FolllowSerializer(data, context=request, many=True)
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
        data = dict()
        favorit = Favorite.objects.filter(
            user_id=request.user.id,
            shopping_cart=True
        ).all()
        for _ in favorit:
            recipe = Recipe.objects.filter(id=_.recipe.id).all()
            for k in recipe:
                a = k.ingredients.all()
                for i in a:
                    if f'{i.ingredient.id}' in data:
                        data[f'{i.ingredient.id}'] += i.amount
                    else:
                        data[f'{i.ingredient.id}'] = i.amount
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        p.setFont('FreeSans', 15, leading=None)
        p.setFillColorRGB(0.29296875, 0.453125, 0.609375)
        p.drawString(260, 800, 'Список покупок')
        p.line(0, 780, 1000, 780)
        p.line(0, 778, 1000, 778)
        x1 = 20
        y1 = 750
        data = dict(sorted(data.items(), key=lambda item: item[1]))
        for k, v in data.items():
            ingredient = Ingredient.objects.get(id=k)

            p.setFont('FreeSans', 15, leading=None)
            p.drawString(
                x1,
                y1-12,
                f'{ingredient.name} ({ingredient.measurement_unit}) - {v}'
            )
            y1 = y1 - 30
        p.setTitle('SetTitle')
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

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
