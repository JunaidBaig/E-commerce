from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('signin', views.signin),
    path('create_list', views.create_list),
    path('upload', views.upload),
    path('show/<int:id>', views.show),
    path('about', views.about),
    path('edit/<int:id>', views.edit_product),
    path('delete/<int:id>', views.delete),
    path('category/<str:string>', views.category),
    path('shop', views.shop)
]