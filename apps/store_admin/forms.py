from django import forms
from apps.products.models import Product, Category, Brand

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name_uz': forms.TextInput(attrs={'class': 'form-input'}),
            'name_ru': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'brand': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brend nomi'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-input'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'description_uz': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'description_ru': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name_uz': forms.TextInput(attrs={'class': 'form-input'}),
            'name_ru': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Emoji or Icon class'}),
        }

