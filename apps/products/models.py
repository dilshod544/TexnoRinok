from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Emoji yoki icon class")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['order', 'name']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        return self.products.filter(is_available=True).count()

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brandlar"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategoriya")
    brand = models.CharField(max_length=100, blank=True, verbose_name="Brend", db_index=True)
    name = models.CharField(max_length=300, verbose_name="Mahsulot nomi")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug (Link nomi)")
    description = models.TextField(verbose_name="To'liq tavsif", blank=True)
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Qisqa tavsif")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Narx (so'm)")
    old_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Eski narx")
    image = models.ImageField(upload_to='products/', verbose_name="Asosiy rasm")
    is_available = models.BooleanField(default=True, verbose_name="Mavjudmi?", db_index=True)
    is_featured = models.BooleanField(default=False, verbose_name="Tanlanganmi?", db_index=True)
    is_bestseller = models.BooleanField(default=False, verbose_name="Xaridorgirmi?", db_index=True)
    stock = models.PositiveIntegerField(default=100, verbose_name="Zaxiradagi miqdor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['is_available', 'is_featured']),
            models.Index(fields=['is_available', 'is_bestseller']),
            models.Index(fields=['is_available', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(discount)
        return 0

    def formatted_price(self):
        return f"{int(self.price):,}".replace(',', ' ')

    def formatted_old_price(self):
        if self.old_price:
            return f"{int(self.old_price):,}".replace(',', ' ')
        return None


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=200, verbose_name="Xususiyat nomi")
    value = models.CharField(max_length=300, verbose_name="Qiymati")

    class Meta:
        verbose_name = "Xususiyat"
        verbose_name_plural = "Xususiyatlar"

    def __str__(self):
        return f"{self.name}: {self.value}"
