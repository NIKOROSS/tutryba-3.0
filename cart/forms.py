from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Order

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if self.product:
            max_quantity = min(self.product.stock, self.product.max_order_quantity or self.product.stock)
            self.fields['quantity'].widget.attrs['max'] = max_quantity
            self.fields['quantity'].widget.attrs['data-max'] = max_quantity
            self.fields['quantity'].validators.append(
                MinValueValidator(1, message='Минимальное количество: 1')
            )
            self.fields['quantity'].validators.append(
                MaxValueValidator(max_quantity, message=f'Максимальное количество: {max_quantity}')
            )

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Адрес доставки'
    )
    promo_code = forms.CharField(
        required=False,
        label='Промокод'
    )

class OrderForm(forms.ModelForm):
    delivery_cost = forms.DecimalField(
        required=False,
        widget=forms.HiddenInput(),
        initial=0
    )
    
    class Meta:
        model = Order
        fields = ['city', 'street', 'house', 'entrance', 'apartment', 'phone', 'comment', 'payment_method']
        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Москва'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: ул. Тверская'
            }),
            'house': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 1'
            }),
            'entrance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 2 (не обязательно)'
            }),
            'apartment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 5 (не обязательно)'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительная информация для курьера (не обязательно)'
            }),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'})
        } 