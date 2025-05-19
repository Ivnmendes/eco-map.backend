from django.urls import path
from .views import UserDetail, UserList, MeView, LoginView, LogoutView, RegisterView, CustomTokenRefreshView
from drf_spectacular.utils import extend_schema

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]

urlpatterns += [
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me')
]