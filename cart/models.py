from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('online', 'Оплата онлайн'),
        ('cash', 'Оплата при получении'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online', verbose_name='Способ оплаты')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    
    # Поля адреса
    city = models.CharField(max_length=100, verbose_name='Город', default='')
    street = models.CharField(max_length=200, verbose_name='Улица', default='')
    house = models.CharField(max_length=20, verbose_name='Дом', default='')
    entrance = models.CharField(max_length=10, blank=True, null=True, verbose_name='Подъезд')
    apartment = models.CharField(max_length=10, blank=True, null=True, verbose_name='Квартира')
    
    # Дополнительные поля
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    @property
    def full_address(self):
        """Полный адрес для отображения"""
        address_parts = [self.city, self.street, f"д. {self.house}"]
        if self.entrance:
            address_parts.append(f"под. {self.entrance}")
        if self.apartment:
            address_parts.append(f"кв. {self.apartment}")
        return ", ".join(address_parts)
    
    def get_total_cost(self):
        """Возвращает общую стоимость заказа"""
        return sum(item.get_total_price() for item in self.items.all())

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
    
    def get_total_price(self):
        """Возвращает общую стоимость товара"""
        return self.price * self.quantity
