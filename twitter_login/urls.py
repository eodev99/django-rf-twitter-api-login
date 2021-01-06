from django.urls import path

from . import views

urlpatterns = [
    path('auth/', views.TwitterCompleteLogin.as_view(), name='twitter_auth'),
    path('auth/reverse/', views.TwitterRequestToken.as_view(), name='twitter_auth_reverse'),
]
