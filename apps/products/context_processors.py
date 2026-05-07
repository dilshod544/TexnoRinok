from django.core.cache import cache
from .models import Category

def categories(request):
    lang = getattr(request, 'LANGUAGE_CODE', 'uz')[:2]
    cache_key = f'menu_categories_{lang}'
    
    menu_categories = cache.get(cache_key)
    if not menu_categories:
        from django.db.models import Count, Q
        menu_categories = list(
            Category.objects.annotate(
                num_products=Count('products', filter=Q(products__is_available=True))
            ).order_by('order', 'name')
        )
        cache.set(cache_key, menu_categories, 60 * 15)
        
    return {
        'menu_categories': menu_categories,
        'CURRENT_LANGUAGE': lang,
    }
