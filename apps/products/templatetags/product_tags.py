from django import template
from django.db.models import Count

register = template.Library()

# Единый источник истины для статических строк интерфейса
UI_TRANSLATIONS = {
    'uz': {
        # Hero
        'hero_badge': '🏆 O\'zbekistonda #1 texnika do\'koni',
        'hero_title': 'Do\'konimizga Xush kelibsiz!',
        'hero_desc': 'Blenderlar, sok apparatlar, mikserlar va boshqa premium oshxona texnikalari.',
        'hero_btn': 'Katalogga o\'tish',
        
        # General UI
        'cart': 'Savat',
        'your_cart': 'Savatingiz',
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
        'products_found': 'ta mahsulot topildi',
        'no_products_category': 'Bu kategoriyada hozircha mahsulotlar yo\'q',
        'check_back_later': 'Tez orada yangi mahsulotlar qo\'shiladi',
        'categories': 'Kategoriyalar',
        'brands': 'Brandlar',
        'price_range': 'Narx oralig\'i',
        'apply': 'Qo\'llash',
        'sort_new': 'Yangi',
        'sort_cheap': 'Arzondan qimmatga',
        'sort_expensive': 'Qimmatdan arzonga',
        'in_stock': 'ta bor',
        'available': 'Mavjud',
        'out_of_stock': 'Tugagan',
        'search': 'Qidiruv',
        'search_placeholder': 'Mahsulotlarni qidirish...',
        'delete': 'O\'chirish',
        'free': 'Bepul',
        'continue_shopping': 'Xaridni davom ettirish',
        'added_to_cart': 'Savatga qo\'shildi!',
        'error': 'Xatolik yuz berdi',
        'search_results': 'qidiruv natijalari',
        'products_count_suffix': 'ta mahsulot',
        'no_products_found': 'Mahsulot topilmadi',
        'try_other_filters': 'Boshqa kalit so\'z yoki filtrlarni sinab ko\'ring',
        'quantity': 'Miqdor',
        'description': 'Tavsif',
        'features': 'Xususiyatlar',
        'related_products': 'O\'xshash mahsulotlar',
        'delivery_time_text': 'Toshkentga 1-2 kunda yetkazish',
        'certified_text': 'Sertifikatlangan mahsulotlar',
        'expert_advice_text': 'Mutaxassis maslahati',
        
        # Auth & Profile
        'registration': 'Ro\'yxatdan o\'tish',
        'welcome_msg': 'Premium do\'konimizga xush kelibsiz',
        'create_account': 'Hisob yaratish',
        'have_account': 'Hisobingiz bormi?',
        'login_system': 'Tizimga kirish',
        'welcome_back': 'Sizni kutgan edik!',
        'no_account': 'Hisobingiz yo\'qmi?',
        'admin_account': 'Siz administrator hisobidasiz',
        'go_to_admin': 'Admin Panelga o\'tish',
        'member': 'A\'zo',
        'personal_info': 'Shaxsiy ma\'lumotlar',
        'birth_date': 'Tug\'ilgan sana',
        'save': 'Saqlash',
        'my_addresses': 'Mening manzillarim',
        'new_address': 'Yangi manzil',
        'edit': 'Tahrirlash',
        'no_addresses': 'Manzillar qo\'shilmagan',
        'orders_history': 'Buyurtmalar tarixi',
        'no_orders': 'Sizda hali buyurtmalar yo\'q',
        'cancel': 'Bekor qilish',
        
        # Cart
        'order_total': 'Buyurtma jami',
        'products_count': 'Mahsulotlar',
        'pcs': 'ta',
        'cart_empty': 'Savatingiz bo\'sh',
        'cart_empty_desc': 'Katalogdan mahsulot tanlang va savatga qo\'shing',
        
        # Order / Checkout
        'checkout_title': 'Buyurtma berish',
        'delivery_info': 'Yetkazib berish ma\'lumotlari',
        'first_name': 'Ism',
        'last_name': 'Familiya',
        'phone': 'Telefon',
        'city': 'Shahar',
        'address': 'Manzil',
        'comment': 'Izoh',
        'confirm_order': 'Buyurtmani tasdiqlash',
        'your_order': 'Sizning buyurtmangiz',
        'total': 'Jami',
        'currency': 'so\'m',
        'order_success': 'Buyurtmangiz qabul qilindi!',
        'order_number': 'Buyurtma raqami',
        'operator_contact': 'tez orada operator siz bilan bog\'lanadi.',
        'back_to_home': 'Bosh sahifaga qaytish',
        'my_orders': 'Mening buyurtmalarim',
        'order': 'Buyurtma',
        'order_status': 'Buyurtma holati',
        'order_details': 'Buyurtma tafsilotlari',
        'cart_contents': 'Savat tarkibi',
        'total_amount': 'Jami summa',
        'receiver': 'Qabul qiluvchi',
        'order_comment': 'Buyurtmaga izoh',
        'order_questions': 'Buyurtma bo\'yicha savollaringiz bo\'lsa, biz bilan bog\'laning.',
        'details': 'Tafsilotlar',
        'start_shopping': 'Xaridni boshlash',
        'order_history_desc': 'Barcha buyurtmalaringiz tarixi va holati',
        
        # Delivery Page
        'service_badge': 'XIZMAT KO\'RSATISH',
        'delivery_service': 'xizmati',
        'delivery_desc_full': 'Biz sizning buyurtmangizni butun O\'zbekiston bo\'ylab eng qisqa vaqtlarda va xavfsiz holatda yetkazib beramiz.',
        'fast_delivery': 'Tezkor yetkazib berish',
        'fast_delivery_desc': 'Toshkent shahri bo\'ylab buyurtmangiz 24 soat ichida eshigingiz tagida bo\'ladi. Biz vaqtingizni qadrlaymiz.',
        'regions_delivery': 'Viloyatlarga yuborish',
        'regions_delivery_desc': 'Viloyat markazlariga yetkazib berish 48-72 soat davomida amalga oshiriladi. BTS yoki boshqa kuryerlik xizmatlari orqali.',
        'delivery_pricing': 'Yetkazib berish narxi',
        'delivery_pricing_desc': 'Toshkent shahri ichida yetkazib berish bepul (50,000 so\'mdan yuqori buyurtmalar uchun). Boshqa hollarda 30,000 so\'m.',
        'have_questions': 'Savollaringiz bormi?',
        'support_desc': 'Bizning qo\'llab-quvvatlash jamoamiz sizga yordam berishga tayyor.',
        'contact_us': 'Biz bilan bog\'lanish',
        
        # Footer
        'footer_desc': 'O\'zbekistondagi eng yaxshi oshxona texnikalari do\'koni. Sifatli mahsulotlar, tez yetkazib berish.',
        'rights': 'Barcha huquqlar himoyalangan.',
        'address_text': 'Toshkent sh., Malika-A8',
    },
    'ru': {
        # Hero
        'hero_badge': '🏆 Магазин техники №1 в Узбекистане',
        'hero_title': 'Добро пожаловать в наш магазин!',
        'hero_desc': 'Блендеры, соковыжималки, миксеры и другая премиальная кухонная техника.',
        'hero_btn': 'Перейти в каталог',
        
        # General UI
        'cart': 'Корзина',
        'your_cart': 'Ваша корзина',
        'add_to_cart': 'Добавить в корзину',
        'buy_now': 'В корзину',
        'catalog': 'Каталог',
        'warranty': 'Гарантия',
        'warranty_desc': '1 год официальной гарантии',
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
        'available': 'В наличии',
        'out_of_stock': 'Нет в наличии',
        'search': 'Поиск',
        'search_placeholder': 'Поиск товаров...',
        'delete': 'Удалить',
        'free': 'Бесплатно',
        'continue_shopping': 'Продолжить покупки',
        'added_to_cart': 'Добавлено в корзину!',
        'error': 'Произошла ошибка',
        'search_results': 'результаты поиска',
        'products_count_suffix': 'товаров',
        'no_products_found': 'Товары не найдены',
        'try_other_filters': 'Попробуйте другие ключевые слова или фильтры',
        'quantity': 'Количество',
        'description': 'Описание',
        'features': 'Характеристики',
        'related_products': 'Похожие товары',
        'delivery_time_text': 'Доставка по Ташкенту 1-2 дня',
        'certified_text': 'Сертифицированные товары',
        'expert_advice_text': 'Консультация специалиста',
        
        # Auth & Profile
        'registration': 'Регистрация',
        'welcome_msg': 'Добро пожаловать в наш премиум магазин',
        'create_account': 'Создать аккаунт',
        'have_account': 'Уже есть аккаунт?',
        'login_system': 'Вход в систему',
        'welcome_back': 'Мы вас ждали!',
        'no_account': 'Нет аккаунта?',
        'admin_account': 'Вы вошли как администратор',
        'go_to_admin': 'Перейти в админ-панель',
        'member': 'Участник',
        'personal_info': 'Личные данные',
        'birth_date': 'Дата рождения',
        'save': 'Сохранить',
        'my_addresses': 'Мои адреса',
        'new_address': 'Новый адрес',
        'edit': 'Редактировать',
        'no_addresses': 'Адреса не добавлены',
        'orders_history': 'История заказов',
        'no_orders': 'У вас пока нет заказов',
        'cancel': 'Отмена',
        
        # Cart
        'order_total': 'Итого по заказу',
        'products_count': 'Товары',
        'pcs': 'шт',
        'cart_empty': 'Ваша корзина пуста',
        'cart_empty_desc': 'Выберите товары в каталоге и добавьте их в корзину',
        
        # Order / Checkout
        'checkout_title': 'Оформление заказа',
        'delivery_info': 'Данные доставки',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'phone': 'Телефон',
        'city': 'Город',
        'address': 'Адрес',
        'comment': 'Комментарий',
        'confirm_order': 'Подтвердить заказ',
        'your_order': 'Ваш заказ',
        'total': 'Итого',
        'currency': 'сум',
        'order_success': 'Ваш заказ принят!',
        'order_number': 'Номер заказа',
        'operator_contact': 'скоро оператор свяжется с вами.',
        'back_to_home': 'Вернуться на главную',
        'my_orders': 'Мои заказы',
        'order': 'Заказ',
        'order_status': 'Статус заказа',
        'order_details': 'Детали заказа',
        'cart_contents': 'Состав корзины',
        'total_amount': 'Итоговая сумма',
        'receiver': 'Получатель',
        'order_comment': 'Комментарий к заказу',
        'order_questions': 'Если у вас есть вопросы по заказу, свяжитесь с нами.',
        'details': 'Подробнее',
        'start_shopping': 'Начать покупки',
        'order_history_desc': 'История и статус всех ваших заказов',
        
        # Delivery Page
        'service_badge': 'ОБСЛУЖИВАНИЕ',
        'delivery_service': 'сервис',
        'delivery_desc_full': 'Мы доставим ваш заказ по всему Узбекистану в кратчайшие сроки и в полной сохранности.',
        'fast_delivery': 'Быстрая доставка',
        'fast_delivery_desc': 'Ваш заказ по Ташкенту будет у вашей двери в течение 24 часов. Мы ценим ваше время.',
        'regions_delivery': 'Доставка в регионы',
        'regions_delivery_desc': 'Доставка в областные центры осуществляется в течение 48-72 часов через BTS или другие курьерские службы.',
        'delivery_pricing': 'Стоимость доставки',
        'delivery_pricing_desc': 'Доставка по Ташкенту бесплатная (для заказов свыше 50,000 сум). В остальных случаях 30,000 сум.',
        'have_questions': 'Есть вопросы?',
        'support_desc': 'Наша служба поддержки готова вам помочь.',
        'contact_us': 'Связаться с нами',
        
        # Footer
        'footer_desc': 'Лучший магазин кухонной техники в Узбекистане. Качественные товары, быстрая доставка.',
        'rights': 'Все права защищены.',
        'address_text': 'г. Ташкент, Малика-А8',
    }
}

@register.simple_tag(takes_context=True)
def ui_translate(context, key):
    request = context.get('request')
    lang_code = 'uz'
    if request:
        lang_code = getattr(request, 'LANGUAGE_CODE', 'uz')
    elif 'LANGUAGE_CODE' in context:
        lang_code = context['LANGUAGE_CODE']
        
    lang_code = lang_code[:2].lower()
    return UI_TRANSLATIONS.get(lang_code, UI_TRANSLATIONS['uz']).get(key, key)

def get_translated_field(obj, field, lang_code):
    if not obj: return ""
    actual_lang = lang_code[:2].lower() if lang_code else 'uz'
    attr_name = f"{field}_{actual_lang}"
    if hasattr(obj, attr_name):
        val = getattr(obj, attr_name)
        if val: return val
    return getattr(obj, field, str(obj))

@register.filter(name='get_translated_name')
def get_translated_name(obj, lang_code=None):
    return get_translated_field(obj, 'name', lang_code)

@register.filter(name='get_translated_description')
def get_translated_description(obj, lang_code=None):
    return get_translated_field(obj, 'description', lang_code)

@register.filter(name='get_translated_value')
def get_translated_value(obj, lang_code=None):
    return get_translated_field(obj, 'value', lang_code)

@register.simple_tag
def get_categories():
    from apps.products.models import Category
    return Category.objects.annotate(num_products=Count('products')).filter(num_products__gt=0)

@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    request = context.get('request')
    if not request: return f"/{lang_code}/"
    
    path = request.path
    from django.urls import resolve, reverse
    from django.utils.translation import activate
    try:
        view = resolve(path)
        activate(lang_code)
        url = reverse(view.view_name, args=view.args, kwargs=view.kwargs)
        return url
    except Exception:
        return f"/{lang_code}/"
