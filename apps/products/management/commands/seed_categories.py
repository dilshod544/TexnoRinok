from django.core.management.base import BaseCommand
from apps.products.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates categories with UZ and RU translations'

    def handle(self, *args, **options):
        categories_data = [
            ("Blender", "Блендер", "🍹"),
            ("Sharbat chiqargich", "Соковыжималка", "🥤"),
            ("Trimmer", "Триммер", "✂️"),
            ("Fen", "Фен", "💨"),
            ("Dyson stayler", "Стайлер Dyson", "✨"),
            ("Havo tozalagich", "Очиститель воздуха", "🍃"),
            ("Go'shtqiymalagich", "Мясорубка", "🥩"),
            ("Aerogril", "Аэрогриль", "🍗"),
            ("Vafli pishirgich", "Вафельница", "🧇"),
            ("Kofemashina", "Кофемашина", "☕"),
            ("Parogenerator", "Парогенератор", "💨"),
            ("Bug'li dazmol (Otparivitel)", "Отпариватель", "👔"),
            ("Tarozi", "Весы", "⚖️"),
            ("Mikser", "Миксер", "🥣"),
            ("Oshxona kombayni", "Кухонный комбайн", "🍲"),
            ("Tish cho'tkasi", "Зубная щетка", "🪥"),
            ("Alisa (Aqlli kolonka)", "Алиса (Умная колонка)", "🔊"),
            ("Toster", "Тостер", "🍞"),
            ("Mikroto'lqinli pech", "Микроволновая печь", "⏲️"),
            ("Changyutgich", "Пылесос", "🧹"),
            ("Robot changyutgich", "Робот-пылесос", "🤖"),
            ("Qo'l changyutgichi", "Ручной пылесос", "🔋"),
            ("Britva", "Бритва", "🪒"),
            ("Epilyator", "Эпилятор", "✨"),
            ("Choper", "Чоппер", "🔪"),
            ("Havo namlagich", "Увлажнитель воздуха", "💧"),
            ("Dazmol", "Утюг", "🧺"),
            ("Choynak", "Чайник", "🫖"),
            ("Kapsulali kofemashina", "Капсульная кофемашина", "☕"),
            ("Massajyor", "Массажер", "💆"),
        ]

        for uz_name, ru_name, icon in categories_data:
            slug = slugify(uz_name)
            category, created = Category.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': uz_name,
                    'name_uz': uz_name,
                    'name_ru': ru_name,
                    'icon': icon
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {uz_name}'))
            else:
                self.stdout.write(self.style.INFO(f'Updated category: {uz_name}'))
