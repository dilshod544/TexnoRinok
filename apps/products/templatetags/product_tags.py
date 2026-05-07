from django import template

register = template.Library()

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
