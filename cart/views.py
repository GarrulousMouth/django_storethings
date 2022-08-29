from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView
from shop.models import Product
from .cart import Cart

# Страница с корзиной
class CartObject(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})

# Добавление элементов в корзину
class CartAdd(CreateView):

    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        return redirect(request.META.get('HTTP_REFERER'))

# Уменьше элементов в корзине
class CartDecrease(TemplateView):

    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove_elem(product=product)
        return redirect('cart_detail')

# Полное удаление элемента из корзины
class CartRemove(TemplateView):
    
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart_detail')