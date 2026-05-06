from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def _invalidate_cart_cache(request):
    """Сбрасываем кэш счётчика корзины в сессии после любого изменения."""
    if 'cart_count_cache' in request.session:
        del request.session['cart_count_cache']


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    _invalidate_cart_cache(request)
    new_count = cart.items.count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'count': new_count, 'message': "Savatga qo'shildi!"})
    return redirect('cart:cart')


@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    _invalidate_cart_cache(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_or_create_cart(request)
        return JsonResponse({'success': True, 'count': cart.items.count(), 'total': str(cart.total)})
    return redirect('cart:cart')


@require_POST
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    _invalidate_cart_cache(request)
    cart = get_or_create_cart(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'subtotal': str(item.subtotal) if quantity > 0 else '0',
            'total': str(cart.total),
            'count': cart.items.count(),
        })
    return redirect('cart:cart')
