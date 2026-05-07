from django import template
from django.db.models import Count

register = template.Library()

# Словарь для ЖЕСТКОГО перевода интерфейса
UI_TRANSLATIONS = {
    'uz': {
        'hero_badge': '🏆 O\'zbekistonda #1 texnika do\'koni',
        'hero_title': 'Do\'konimizga Xush kelibsiz!',
        'hero_desc': 'Blenderlar, sok apparatlar, mikсерlar va boshqa premium oshxona texnikalari.',
        'hero_btn': 'Katalogga o\'tish',
        'cart': 'Savat',
        'add_to_cart': 'Savatga qo\'shish',
        'buy_now': 'Savatga',
        'catalog': 'Katalog',
        'home': 'Asosiy',
        'news': 'Yangiliklar',
        'delivery': 'Yetkazib berish',
        'contact': 'Bog\'lanish',
        'profile': 'Profil',
        'login': 'Kirish',
        'logout': 'Chiqish',
        'all_products': 'Barcha mahsulotlar',
        'categories': 'Kategoriyalar',
        'brands': 'Brandlar',
        'price_range': 'Narx oralig\'i',
        'apply': 'Qo\'llash',
        'sort_new': 'Yangi',
        'sort_cheap': 'Arzondan qimmatga',
        'sort_expensive': 'Qimmatdan arzonga',
        'in_stock': 'ta bor',
        'out_of_stock': 'Tugagan',
    },
    'ru': {
        'hero_badge': '🏆 Магазин техники №1 в Узбекистане',
        'hero_title': 'Добро пожаловать в наш магазин!',
        'hero_desc': 'Блендеры, соковыжималки, миксеры и другая премиальная кухонная техника.',
        'hero_btn': 'Перейти в каталог',
        'cart': 'Корзина',
        'add_to_cart': 'Добавить в корзину',
        'buy_now': 'В корзину',
        'catalog': 'Каталог',
        'home': 'Главная',
        'news': 'Новинки',
        'delivery': 'Доставка',
        'contact': 'Контакты',
        'profile': 'Профиль',
        'login': 'Войти',
        'logout': 'Выйти',
        'all_products': 'Все товары',
        'categories': 'Категории',
        'brands': 'Бренды',
        'price_range': 'Цена',
        'apply': 'Применить',
        'sort_new': 'Новинки',
        'sort_cheap': 'Сначала дешевые',
        'sort_expensive': 'Сначала дорогие',
        'in_stock': 'в наличии',
        'out_of_stock': 'Нет в наличии',
    }
}

@register.simple_tag(takes_context=True)
def ui_translate(context, key):
    """Принудительный перевод статического текста с определением языка из контекста"""
    request = context.get('request')
    lang_code = 'uz'
    if request:
        lang_code = getattr(request, 'LANGUAGE_CODE', 'uz')
    
    # Если lang_code длинный (напр. 'ru-ru'), берем первые две буквы
    lang_code = lang_code[:2].lower()
    
    return UI_TRANSLATIONS.get(lang_code, UI_TRANSLATIONS['uz']).get(key, key)

@register.filter
def get_translated_name(obj, lang_code):
    if not obj: return ""
    # Определяем язык более надежно
    actual_lang = lang_code[:2].lower() if lang_code else 'uz'
    attr_name = f"name_{actual_lang}"
    if hasattr(obj, attr_name):
        val = getattr(obj, attr_name)
        if val: return val
    return getattr(obj, 'name', str(obj))

@register.simple_tag
def get_categories():
    from apps.products.models import Category
    return Category.objects.annotate(num_products=Count('products')).filter(num_products__gt=0)

@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    path = context.get('request').path
    from django.urls import resolve, reverse
    from django.utils.translation import activate
    try:
        view = resolve(path)
        activate(lang_code)
        url = reverse(view.view_name, args=view.args, kwargs=view.kwargs)
        return url
    except Exception:
        return f"/{lang_code}/"
