from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView
from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.cart import Cart

# Страница заказов пользователя
class OrdersPage(ListView):
    template_name = 'orders/orders.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        products = OrderItem.objects.filter(order__in=orders)
        return render(request, self.template_name, {'orders': orders, 'products': products})

# Создание заказа
class OrderCreate(CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderCreateForm

    def get(self, request):
        form = self.form_class
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart, 'form': form})

    def post(self, request):
        cart = Cart(request)
        form = self.form_class(request.POST)
        if form.is_valid():
            # Возвращение объекта без сохранения с commit
            order = form.save(commit=False)
            # Присвоение заказа пользователю
            order.user = request.user
            order.save()
            # Создание объектов заказа из корзины
            for item in cart:
                OrderItem.objects.create(order=order, 
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # Очистка корзины
            cart.clear()
            return render(request, 'orders/order_created.html', {'order': order})

# Обновление заказа, если пользователь его завершил
class OrderFinished(TemplateView):

    def get(self, request, order_id):
        Order.objects.filter(id=order_id).update(finished=True)
        return redirect('orders')
