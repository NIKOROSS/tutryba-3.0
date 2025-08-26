from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if update_quantity:
            if quantity > product.stock:
                raise ValueError(f'Недостаточно товара {product.name} на складе')
            self.cart[product_id]['quantity'] = quantity
        else:
            new_quantity = self.cart[product_id]['quantity'] + quantity
            if new_quantity > product.stock:
                raise ValueError(f'Недостаточно товара {product.name} на складе')
            self.cart[product_id]['quantity'] = new_quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            product_id = str(product.id)
            if product_id in self.cart:
                # Создаем новый словарь для каждого элемента, не изменяя сессию
                item = {
                    'product': product,
                    'quantity': self.cart[product_id]['quantity'],
                    'price': str(Decimal(self.cart[product_id]['price'])),
                    'total_price': str(Decimal(self.cart[product_id]['price']) * self.cart[product_id]['quantity'])
                }
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return str(total)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True 