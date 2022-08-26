from django.urls import path
from .views import Favourites, FavouritesAdd

urlpatterns = [
    path('', Favourites.as_view(), name='favourites'),
    path('add/<int:product_id>/', FavouritesAdd.as_view(), name='favourites_add'),
]