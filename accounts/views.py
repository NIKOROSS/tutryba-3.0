from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from cart.models import Order
from .forms import UserUpdateForm

# Create your views here.

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        messages.success(request, 'Профиль успешно обновлен')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile_edit.html')

@login_required
def order_history(request):
    orders = request.user.orders.all()
    return render(request, 'accounts/order_history.html', {'orders': orders})
