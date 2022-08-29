from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        # Создание сессии с корзиной
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Присвоение корзине пустого словаря
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Метод для добавления элемента в корзину
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # Удаление одного элемента из корзины, если их там несколько
    def remove_elem(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1
            self.save()
        else:
            self.remove(product)

    # Сохранение корзины в сессии
    def save(self):
        """
        Сохранение корзины в сессии
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    # Полное удаление элемента из корзины, независимо от количества
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # Перебор элементов, содержащихся в корзине
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        # Проход по элементам корзины и создание общей суммы
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Возврат количества элементов в корзине
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Получение суммы всей покупки
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # Очищение корзины
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True