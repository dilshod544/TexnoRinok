from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from apps.products.models import Product, Category, Brand

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'brand', 'slug', 'description', 'short_description', 
                  'price', 'old_price', 'image', 'is_available', 'is_featured', 'is_bestseller', 'stock')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Mahsulot nomi'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'brand': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brend nomi'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-input'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'short_description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'image': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'is_bestseller': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image and not self.instance.pk:
            raise ValidationError("Mahsulot rasmi talab qilinadi.")
        if image and image.size > 5 * 1024 * 1024:
            raise ValidationError("Rasm hajmi 5MB dan katta bo'lmasligi kerak.")
        return image

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        name = self.cleaned_data.get('name', '').strip()
        
        # Auto-generate slug from name if not provided
        if not slug and name:
            slug = slugify(name, allow_unicode=True)
        
        if not slug:
            raise ValidationError("Slug talab qilinadi yoki mahsulot nomi bo'sh bo'lmasligi kerak.")
        
        normalized_slug = slugify(slug, allow_unicode=True)
        if not normalized_slug:
            raise ValidationError("Slug noto'g'ri formatda. Iltimos, boshqa slug kiriting.")

        qs = Product.objects.exclude(pk=self.instance.pk) if self.instance.pk else Product.objects.all()
        if qs.filter(slug=normalized_slug).exists():
            raise ValidationError("Bu slug allaqachon mavjud. Iltimos, boshqa slug kiriting.")

        self.cleaned_data['slug'] = normalized_slug
        return normalized_slug

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'icon', 'image', 'order')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Emoji or Icon class'}),
            'image': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
        }

