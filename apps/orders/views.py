from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.cart.views import get_or_create_cart
from .models import Order, OrderItem
from .forms import OrderForm


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.item_count:
        messages.warning(request, "Savatingiz bo'sh!")
        return redirect('cart:cart')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            initial_data['phone'] = request.user.profile.phone_number

    form = OrderForm(request.POST or None, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        if request.user.is_authenticated:
            order.user = request.user
        order.total_price = cart.total
        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
        cart.items.all().delete()

        # Basic notification logic placeholder
        send_order_sms_notification(order)

        return redirect('orders:success', pk=order.pk)

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

from .utils import send_sms

def send_order_sms_notification(order):
    """
    Sends an SMS to order.phone to confirm their order.
    """
    message = f"TexnoRinok: Buyurtmangiz qabul qilindi! Buyurtma #{order.pk}. Tez orada operator bog'lanadi."
    send_sms(order.phone, message)


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/success.html', {'order': order})


def order_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/list.html', {'orders': orders})


def order_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})
