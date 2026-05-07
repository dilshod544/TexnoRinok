from django import template

register = template.Library()

@register.filter
def get_translated_name(obj, lang_code):
    # modeltranslation automatically returns the correct field (e.g. name_ru) 
    # when accessing the base field (e.g. name) if the language is active.
    return obj.name
