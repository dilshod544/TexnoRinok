from django import template

register = template.Library()

@register.filter
def get_translated_name(category, lang_code):
    return category.get_translated_name(lang_code)
