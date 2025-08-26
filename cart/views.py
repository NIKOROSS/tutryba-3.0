from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm, OrderForm
from .models import Order, OrderItem
from .delivery_service import delivery_service
from django.db import transaction
from decimal import Decimal

@require_POST
def add_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        try:
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
            return JsonResponse({
                'status': 'success',
                'message': f'Товар {product.name} успешно добавлен в корзину',
                'cart_total': len(cart)
            })
        except ValueError as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Неверные данные формы'
        })

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

@require_POST
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    
    if action == 'increase':
        cart.add(product=product, quantity=1, update_quantity=False)
    elif action == 'decrease':
        current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
        if current_quantity > 1:
            cart.add(product=product, quantity=current_quantity - 1, update_quantity=True)
        else:
            cart.remove(product)
    
    return redirect('cart:cart_detail')

@login_required
@transaction.atomic
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            
            # Добавляем стоимость доставки к общей сумме
            delivery_cost = form.cleaned_data.get('delivery_cost', 0)
            cart_total = cart.get_total_price()
            
            # Преобразуем cart_total в Decimal
            if isinstance(cart_total, str):
                cart_total = Decimal(cart_total.replace(' ₽', ''))
            elif isinstance(cart_total, float):
                cart_total = Decimal(str(cart_total))
            elif isinstance(cart_total, Decimal):
                pass  # уже Decimal
            else:
                cart_total = Decimal(str(cart_total))
            
            # Преобразуем delivery_cost в Decimal
            if isinstance(delivery_cost, (int, float)):
                delivery_cost = Decimal(str(delivery_cost))
            elif isinstance(delivery_cost, str):
                delivery_cost = Decimal(delivery_cost)
            elif isinstance(delivery_cost, Decimal):
                pass  # уже Decimal
            else:
                delivery_cost = Decimal('0')
            
            order.total_amount = cart_total + delivery_cost
            
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            cart.clear()
            messages.success(request, f'Заказ успешно оформлен! Стоимость доставки: {delivery_cost} ₽')
            return redirect('cart:order_success')
    else:
        form = OrderForm()
    
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'form': form
    })

def order_success(request):
    return render(request, 'cart/order_success.html')

def calculate_delivery(request):
    """
    AJAX представление для расчета стоимости доставки
    """
    if request.method == 'POST':
        # Собираем адрес из отдельных полей
        city = request.POST.get('city', '').strip()
        street = request.POST.get('street', '').strip()
        house = request.POST.get('house', '').strip()
        entrance = request.POST.get('entrance', '').strip()
        apartment = request.POST.get('apartment', '').strip()
        
        # Формируем полный адрес
        address_parts = [city, street, f"д. {house}"]
        if entrance:
            address_parts.append(f"под. {entrance}")
        if apartment:
            address_parts.append(f"кв. {apartment}")
        
        delivery_address = ", ".join(address_parts)
        
        if not city or not street or not house:
            return JsonResponse({
                'success': False,
                'error': 'Заполните обязательные поля: город, улица, дом'
            })
        
        # Рассчитываем вес заказа (примерно)
        cart = Cart(request)
        total_weight = sum(item['quantity'] * 0.5 for item in cart)  # 0.5 кг на единицу товара
        
        # Рассчитываем стоимость доставки
        result = delivery_service.calculate_delivery_cost(delivery_address, total_weight)
        
        return JsonResponse(result)
    
    return JsonResponse({
        'success': False,
        'error': 'Неверный метод запроса'
    })
