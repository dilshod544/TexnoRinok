from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
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

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        if not slug:
            return slug

        normalized_slug = slugify(slug, allow_unicode=True)
        if not normalized_slug:
            raise ValidationError("Slug noto'g'ri formatda. Iltimos, boshqa slug kiriting.")

        qs = Product.objects.exclude(pk=self.instance.pk) if self.instance.pk else Product.objects.all()
        if qs.filter(slug=normalized_slug).exists():
            raise ValidationError("Bu slug allaqachon mavjud. Iltimos, boshqa slug kiriting.")

        return normalized_slug

    def clean(self):
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug', '').strip()
        if not slug:
            name = cleaned_data.get('name') or cleaned_data.get('name_uz') or cleaned_data.get('name_ru')
            if name:
                cleaned_data['slug'] = slugify(name, allow_unicode=True)
        return cleaned_data

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

