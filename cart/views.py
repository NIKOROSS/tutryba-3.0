from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm, OrderForm
from .models import Order, OrderItem
from django.db import transaction

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
            order.total_amount = cart.get_total_price()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            cart.clear()
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('cart:order_success')
    else:
        form = OrderForm()
    
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'form': form
    })

def order_success(request):
    return render(request, 'cart/order_success.html')
