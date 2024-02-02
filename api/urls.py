from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path("homepage/<str:language>", views.homepage, name="homepage"),
    path("search/<str:search_input>", views.search, name="search"),
    path('articles/', views.articles, name='articles'),
    path('articles/<str:language>/<str:slug>/', views.article, name='article'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register')
]
