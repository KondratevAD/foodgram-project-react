from django.urls import include, path
from djoser import views as djoser_views
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='UserView')

urlpatterns = [
    path(
        'v1/users/set_password/',
        djoser_views.UserViewSet.as_view({'post': 'set_password'}),
        name='userSetPassword'
    ),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls.authtoken')),
]
