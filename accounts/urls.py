from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('activate/', views.activate, name='activate'),
    path('activateAccount/<uidb64>/<token>/',
         views.activateAccount, name='activateAccount'),
]
