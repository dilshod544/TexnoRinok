from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.core.cache import cache
from django.core.paginator import Paginator
from .models import Product, Category, Brand


def home(request):
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
    cache_key = f'home_context_{lang}'
    context = cache.get(cache_key)
    if not context:
        # list() is important to evaluate the queryset before caching
        featured_products = list(
            Product.objects.select_related('category')
            .filter(is_available=True, is_featured=True)[:8]
        )
        bestsellers = list(
            Product.objects.select_related('category')
            .filter(is_available=True, is_bestseller=True)[:8]
        )
        categories_list = list(
            Category.objects.annotate(
                num_products=Count('products', filter=Q(products__is_available=True))
            ).order_by('order', 'name')[:6]
        )
        new_arrivals = list(
            Product.objects.select_related('category')
            .filter(is_available=True).order_by('-created_at')[:8]
        )
        context = {
            'featured_products': featured_products,
            'bestsellers': bestsellers,
            'categories': categories_list,
            'new_arrivals': new_arrivals,
        }
        cache.set(cache_key, context, 60 * 5)

    return render(request, 'products/home.html', context)


def product_list(request):
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
    cache_key = f'menu_categories_{lang}'
    categories_list = cache.get(cache_key)
    if not categories_list:
        categories_list = list(
            Category.objects.annotate(
                num_products=Count('products', filter=Q(products__is_available=True))
            ).order_by('order', 'name')
        )
        cache.set(cache_key, categories_list, 60 * 15)

    brands = cache.get('all_brands')
    if not brands:
        brands = list(Brand.objects.all())
        cache.set('all_brands', brands, 3600)

    products = Product.objects.select_related('category').filter(is_available=True)

    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    search = request.GET.get('q')
    sort = request.GET.get('sort', '-created_at')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    active_category = None
    if category_slug:
        # Ищем из уже закэшированного списка — без доп. запроса в БД
        active_category = next((c for c in categories_list if c.slug == category_slug), None)
        if active_category:
            products = products.filter(category=active_category)

    if brand_slug:
        products = products.filter(brand=brand_slug)

    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass

    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        '-created_at': '-created_at',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'categories': categories_list,
        'brands': brands,
        'active_category': active_category,
        'search': search,
        'sort': sort,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('features', 'images'),
        slug=slug,
        is_available=True,
    )
    related = list(
        Product.objects.select_related('category')
        .filter(category=product.category, is_available=True)
        .exclude(pk=product.pk)[:4]
    )
    context = {
        'product': product,
        'related': related,
    }
    return render(request, 'products/detail.html', context)


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = (
        Product.objects.select_related('category')
        .filter(category=category, is_available=True)
        .order_by('-created_at')
    )
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'category': category,
        'products': page_obj,
    }
    return render(request, 'products/category.html', context)


def delivery_view(request):
    return render(request, 'products/delivery.html')


def contact_view(request):
    return render(request, 'products/contact.html')
