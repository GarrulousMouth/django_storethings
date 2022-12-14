from django.urls import path
from .views import HomeView, Product

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:category_slug>', HomeView.as_view(), name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>', Product.as_view(), name='product_detail'),
]
