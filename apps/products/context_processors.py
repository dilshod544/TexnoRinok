from django.core.cache import cache
from .models import Category

def categories(request):
    menu_categories = cache.get('menu_categories')
    if not menu_categories:
        menu_categories = list(Category.objects.all())  # list() muhim!
        cache.set('menu_categories', menu_categories, 60 * 15)
    return {'menu_categories': menu_categories}
