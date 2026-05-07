from django import template
from django.db.models import Count

register = template.Library()

@register.filter
def get_translated_name(obj, lang_code):
    """
    Returns the translated name field (e.g. name_ru or name_uz).
    """
    if not obj:
        return ""
    
    # Try name_ru, name_uz etc.
    attr_name = f"name_{lang_code}"
    if hasattr(obj, attr_name):
        val = getattr(obj, attr_name)
        if val:
            return val
            
    # Fallback to base name
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
