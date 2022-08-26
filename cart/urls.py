from django.urls import path
from .views import CartAdd, CartObject, CartRemove, CartDecrease

urlpatterns = [
    path('', CartObject.as_view(), name='cart_detail'),
    path('add/<int:product_id>', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>', CartRemove.as_view(), name='cart_remove'),
    path('decrease/<int:product_id>', CartDecrease.as_view(), name='cart_decrease'),
]