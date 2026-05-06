from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, ProductFeature, Brand

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description')

@register(ProductFeature)
class ProductFeatureTranslationOptions(TranslationOptions):
    fields = ('name', 'value')
