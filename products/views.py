from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Product, Category
from cart.forms import CartAddProductForm

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    cart_product_form = CartAddProductForm()
    return render(request, 'products/home.html', {
        'categories': categories,
        'products': products,
        'cart_product_form': cart_product_form,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm(product=product)
    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'products/category_detail.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })
