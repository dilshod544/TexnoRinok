from django.core.cache import cache
from .models import Category

def categories(request):
    menu_categories = cache.get('menu_categories')
    if not menu_categories:
        from django.db.models import Count, Q
        menu_categories = list(
            Category.objects.annotate(
                num_products=Count('products', filter=Q(products__is_available=True))
            ).order_by('order', 'name')
        )
        cache.set('menu_categories', menu_categories, 60 * 15)
    return {'menu_categories': menu_categories}
