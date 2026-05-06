from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Address
from django.core.validators import RegexValidator

def style_form_fields(form):
    """Вспомогательная функция для стилизации полей формы"""
    for field_name, field in form.fields.items():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.update({'class': 'form-checkbox'})
        else:
            existing_classes = field.widget.attrs.get('class', '')
            if 'form-input' not in existing_classes:
                new_class = f"{existing_classes} form-input".strip()
                field.widget.attrs.update({'class': new_class})

class CustomUserCreationForm(UserCreationForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(
        validators=[phone_regex], 
        max_length=17, 
        required=True, 
        label="Telefon raqamingiz",
        widget=forms.TextInput(attrs={'placeholder': '+998901234567'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={'phone_number': self.cleaned_data['phone_number']}
            )
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['label', 'full_name', 'phone', 'city', 'address', 'is_default']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Ism Familiya'}),
            'phone': forms.TextInput(attrs={'placeholder': '+998XXXXXXXXX'}),
            'city': forms.TextInput(attrs={'placeholder': 'Toshkent'}),
            'address': forms.Textarea(attrs={'placeholder': 'Ko\'cha, uy raqami...', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        style_form_fields(self)
