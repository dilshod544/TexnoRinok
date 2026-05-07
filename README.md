# TexnoRinok — Django Oshxona Texnikalari Do'koni

## Loyiha Arxitekturasi

```
techshop/
├── techshop/           # Asosiy konfiguratsiya
│   ├── settings.py     # Sozlamalar
│   ├── urls.py         # Asosiy URL-lar
│   └── wsgi.py
├── apps/
│   ├── products/       # Mahsulotlar (models, views, urls, admin)
│   ├── cart/           # Savat + context processor
│   ├── orders/         # Buyurtmalar + forma
│   └── accounts/       # Foydalanuvchilar (login/register)
├── templates/
│   ├── base/base.html  # Asosiy shablon
│   ├── products/       # Mahsulot sahifalari
│   ├── cart/           # Savat
│   ├── orders/         # Buyurtma + muvaffaqiyat
│   └── accounts/       # Login/Register
├── static/
│   ├── css/main.css    # To'liq dizayn tizimi
│   └── js/main.js      # JavaScript (AJAX, animatsiyalar)
├── requirements.txt
└── manage.py
```

## O'rnatish

```bash
# 1. Virtual muhit yarating
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Paketlarni o'rnating
pip install -r requirements.txt

# 3. Ma'lumotlar bazasini migratsiya qiling
python manage.py makemigrations
python manage.py migrate

# 4. Superuser yarating (admin uchun)
python manage.py createsuperuser

# 5. Statik fayllarni yig'ing
python manage.py collectstatic

# 6. Serverni ishga tushiring
python manage.py runserver
```

## Admin panelida kategoriyalar qo'shish

http://localhost:8000/admin/ ga kiring va:
1. **Categories** → Qo'shing: "Blenderlar", "Sok apparatlar", "Mikserlar" va h.k.
2. **Brands** → Qo'shing: "Bosch", "Philips", "Samsung" va h.k.
3. **Products** → Mahsulotlar qo'shing

## Dizayn Tizimi

- **Rang sxemasi**: Qorong'u fon (#0d0d0f) + To'q sariq (#ff6b2b) aktsent
- **Shriftlar**: Syne (sarlavha) + DM Sans (matn)
- **Responsive**: Mobil, planshet va desktop uchun optimallashtirilgan
- **Animatsiyalar**: CSS animatsiyalar + IntersectionObserver
- **AJAX savat**: Sahifani yangilashsiz mahsulot qo'shish

## To'lov tizimlari (kelajakda qo'shish uchun)

- Click: https://docs.click.uz
- Payme: https://developer.payme.uz
- Uzum Bank: https://uzumbank.uz/developers
