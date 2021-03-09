from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.main),
    path('allbeers', views.allbeers),
    path('beerform', views.beerform),
    path('addbeer', views.addBeer),
    path('filterstate', views.filterstate),
    path('filtercity', views.filtercity),
    path('filterbeer', views.filterbeer),
    path('filterforms', views.filterform),
    path('beerTable/<int:beer_id>/edit', views.editbeer),
    path('beerTable/<int:beer_id>/updatebeer', views.updateBeer),
    path('beerTable/<int:beer_id>/delete', views.deletebeer)
]