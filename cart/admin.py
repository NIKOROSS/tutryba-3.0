from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['price']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'full_address', 'phone', 'payment_method', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'city', 'street', 'phone']
    readonly_fields = ['total_amount', 'created_at', 'updated_at', 'full_address']
    list_editable = ['status']
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'status', 'payment_method', 'total_amount')
        }),
        ('Адрес доставки', {
            'fields': ('city', 'street', 'house', 'entrance', 'apartment', 'full_address')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'comment')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [OrderItemInline]
