from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city', 'comment']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ismingiz', 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiyangiz', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+998 XX XXX XX XX', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com', 'class': 'form-input'}),
            'address': forms.Textarea(attrs={'placeholder': "Ko'cha, uy raqami...", 'rows': 3, 'class': 'form-input'}),
            'city': forms.TextInput(attrs={'placeholder': 'Toshkent', 'class': 'form-input'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Qo\'shimcha ma\'lumot...', 'rows': 2, 'class': 'form-input'}),
        }
    def clean_city(self):
        city = self.cleaned_data.get('city')
        valid_cities = ['toshkent', 'tashkent', 'ташкент', 'тошкент']
        if city.lower() not in valid_cities:
            raise forms.ValidationError("Yetkazib berish faqat Toshkent shahri bo'ylab amalga oshiriladi.")
        return city
