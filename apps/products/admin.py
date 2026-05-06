from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import Category, Brand, Product, ProductImage, ProductFeature

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

class ProductFeatureInline(TranslationTabularInline):
    model = ProductFeature
    extra = 3

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['name', 'icon', 'slug', 'order', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']

@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ['image_preview', 'name', 'category', 'brand', 'price', 'stock', 'is_available', 'is_featured', 'is_bestseller']
    list_filter = ['category', 'brand', 'is_available', 'is_featured', 'is_bestseller']
    list_editable = ['price', 'stock', 'is_available', 'is_featured', 'is_bestseller']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductFeatureInline]

    def image_preview(self, obj):
        from django.utils.html import mark_safe
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "No Image"
    image_preview.short_description = 'Image'
