from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, AddressForm
from .models import Address, Profile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Ro'yxatdan o'tdingiz!")
        return redirect('products:home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Xush kelibsiz!")
        return redirect(request.GET.get('next', 'products:home'))
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('products:home')


@login_required
def profile_view(request):
    # Ensure profile exists
    Profile.objects.get_or_create(user=request.user)
    
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, instance=request.user.profile)
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Profilingiz yangilandi!")
                return redirect('accounts:profile')

    addresses = request.user.addresses.all()
    orders = request.user.order_set.all().order_by('-created_at')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'addresses': addresses,
        'orders': orders,
        'active_tab': request.GET.get('tab', 'info')
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def address_create(request):
    form = AddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        messages.success(request, "Manzil qo'shildi!")
        return redirect('accounts:profile')
    return render(request, 'accounts/address_form.html', {'form': form, 'title': "Yangi manzil"})

@login_required
def address_update(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    form = AddressForm(request.POST or None, instance=address)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Manzil yangilandi!")
        return redirect('accounts:profile')
    return render(request, 'accounts/address_form.html', {'form': form, 'title': "Manzilni tahrirlash"})

@login_required
@require_POST
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, "Manzil o'chirildi!")
    return redirect('accounts:profile')
