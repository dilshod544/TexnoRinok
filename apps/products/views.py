from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Brand


from django.core.cache import cache

def home(request):
    # Try to get data from cache
    context = cache.get('home_context')
    if not context:
        featured_products = Product.objects.select_related('category').filter(is_available=True, is_featured=True)[:8]
        bestsellers = Product.objects.select_related('category').filter(is_available=True, is_bestseller=True)[:8]
        categories = Category.objects.all()[:6]
        new_arrivals = Product.objects.select_related('category').filter(is_available=True).order_by('-created_at')[:8]
        context = {
            'featured_products': featured_products,
            'bestsellers': bestsellers,
            'categories': categories,
            'new_arrivals': new_arrivals,
        }
        cache.set('home_context', context, 60 * 5)  # Cache for 5 minutes
    
    return render(request, 'products/home.html', context)


def product_list(request):
    # Cache categories and brands for sidebar (1 hour)
    categories = cache.get('all_categories')
    if not categories:
        categories = list(Category.objects.all())
        cache.set('all_categories', categories, 3600)
        
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
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            products = products.filter(category=active_category)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        '-created_at': '-created_at',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'active_category': active_category,
        'search': search,
        'sort': sort,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk)[:4]
    context = {
        'product': product,
        'related': related,
    }
    return render(request, 'products/detail.html', context)


def category_view(request, slug):
    category = Category.objects.filter(slug=slug).first()
    if not category:
        return redirect('products:list')
    products = Product.objects.filter(category=category, is_available=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category.html', context)


def delivery_view(request):
    return render(request, 'products/delivery.html')


def contact_view(request):
    return render(request, 'products/contact.html')
