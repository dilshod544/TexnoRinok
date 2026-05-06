from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")

    def __str__(self):
        return f"{self.user.username}'s profile"


class Address(models.Model):
    LABEL_CHOICES = [
        ('home',  '🏠 Uy'),
        ('work',  '💼 Ish joyi'),
        ('other', '📍 Boshqa'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label      = models.CharField(max_length=20, choices=LABEL_CHOICES, default='home', verbose_name="Tur")
    full_name  = models.CharField(max_length=200, verbose_name="Ism Familiya")
    phone      = models.CharField(max_length=17, verbose_name="Telefon")
    city       = models.CharField(max_length=100, default='Toshkent', verbose_name="Shahar")
    address    = models.TextField(verbose_name="Manzil")
    is_default = models.BooleanField(default=False, verbose_name="Asosiy manzil")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.get_label_display()}: {self.address[:50]}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
