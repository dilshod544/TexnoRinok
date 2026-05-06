from .models import Cart


def cart_count(request):
    """
    Кэшируем счётчик корзины в сессии — избегаем 2 DB запроса на каждой странице.
    Сессионный кэш сбрасывается при изменении корзины (в views корзины).
    """
    count = 0
    try:
        if request.user.is_authenticated:
            # Для авторизованных — кэшируем в сессии
            count = request.session.get('cart_count_cache')
            if count is None:
                cart = Cart.objects.filter(user=request.user).first()
                count = cart.items.count() if cart else 0
                request.session['cart_count_cache'] = count
        else:
            session_key = request.session.session_key
            if session_key:
                count = request.session.get('cart_count_cache', 0)
                if count == 0:
                    cart = Cart.objects.filter(session_key=session_key).first()
                    count = cart.items.count() if cart else 0
    except Exception:
        pass
    return {'cart_count': count}
