from django.urls import path
from .views import OrderCreate, OrdersPage, OrderFinished

urlpatterns = [
    path('', OrdersPage.as_view(), name='orders'),
    path('create', OrderCreate.as_view(), name='order_create'),
    path('finished/<int:order_id>', OrderFinished.as_view(), name='order_finished'),

]