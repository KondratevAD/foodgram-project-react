from django.urls import include, path, re_path
from djoser import views as djoser_views
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='UserView')
router_v1.register('tags', views.TagViewSet, basename='TagView')
router_v1.register(
    'ingredients',
    views.IngredientViewSet,
    basename='IngredientView'
)
router_v1.register('recipes', views.RecipeViewSet, basename='RecipeView')

urlpatterns = [
    path(
        'users/set_password/',
        djoser_views.UserViewSet.as_view({'post': 'set_password'}),
        name='userSetPassword'
    ),
    # path(
    #     'users/subscriptions/',
    #     views.subscriptions,
    #     name='SubscriptionsView'
    # ),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    re_path(
        r'recipes/(?P<id>[0-9]+)/shopping_cart',
        views.shopping_cart,
        name='ShoppingView'
    ),
    re_path(
        r'recipes/(?P<id>[0-9]+)/favorite',
        views.favorite,
        name='FavoriteView'
    ),
    re_path(
        r'users/(?P<id>[0-9]+)/subscribe',
        views.follow,
        name='FollowView'
    )
]
