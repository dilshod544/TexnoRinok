from django.core.cache import cache
from .models import Category

def categories(request):
    menu_categories = cache.get('menu_categories')
    if not menu_categories:
        menu_categories = Category.objects.all()
        cache.set('menu_categories', menu_categories, 60 * 15)  # Cache for 15 minutes
    
    return {
        'menu_categories': menu_categories
    }
