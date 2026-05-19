from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from decouple import config
import logging
from apps.orders.models import Order
from apps.products.models import Product, Category, Brand
from .forms import ProductAdminForm, CategoryAdminForm

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('store_admin:dashboard')
        logout(request)
    
    if request.method == 'POST':
        # Step 2: Verify Static Security Key
        if 'verify_code' in request.POST:
            user_id = request.session.get('pending_admin_id')
            if not user_id:
                messages.error(request, "Sessiya muddati tugagan. Iltimos, qaytadan login qiling.")
                return redirect('store_admin:login')
                
            # Get secret code from environment
            admin_secret = config('ADMIN_PANEL_SECRET', default='qadirdonlar12')
            
            if request.POST.get('code') == admin_secret:
                try:
                    user = User.objects.get(pk=user_id)
                    login(request, user)
                    if 'pending_admin_id' in request.session: 
                        del request.session['pending_admin_id']
                    return redirect('store_admin:dashboard')
                except User.DoesNotExist:
                    messages.error(request, "Foydalanuvchi topilmadi.")
                    return redirect('store_admin:login')
            else:
                messages.error(request, "Xato xavfsizlik kaliti kiritildi.")
                return render(request, 'store_admin/login_verify.html')

        # Step 1: Login Credentials
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                request.session['pending_admin_id'] = user.id
                return render(request, 'store_admin/login_verify.html')
            messages.error(request, "Faqat administratorlar kirishi mumkin.")
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = AuthenticationForm()
    return render(request, 'store_admin/login_simple.html', {'form': form})

@user_passes_test(is_admin, login_url='store_admin:login')
def dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(created_at__gte=today_start).count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    recent_orders = Order.objects.order_by('-created_at')[:5]

    # Advanced Analytics
    one_month_ago = now - timedelta(days=30)
    revenue_last_month = Order.objects.filter(created_at__gte=one_month_ago).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    from django.db.models import Count
    top_categories = Category.objects.annotate(num_products=Count('products')).order_by('-num_products')[:5]
    
    status_counts = Order.objects.values('status').annotate(count=Count('status'))
    
    context = {
        'total_orders': total_orders,
        'today_orders': today_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'revenue_last_month': revenue_last_month,
        'top_categories': top_categories,
        'status_counts': status_counts,
    }
    return render(request, 'store_admin/dashboard.html', context)

@user_passes_test(is_admin, login_url='store_admin:login')
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store_admin/product_list.html', {'products': products})

@user_passes_test(is_admin, login_url='store_admin:login')
def product_add(request):
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save()
                messages.success(request, f"✅ Mahsulot '{product.name}' muvaffaqiyatli qo'shildi.")
                return redirect('store_admin:product_list')
            except IntegrityError as e:
                logger.error(f"IntegrityError while adding product: {e}")
                form.add_error('slug', "Slug allaqachon mavjud. Iltimos, boshqa slug kiriting.")
            except Exception as e:
                logger.error(f"Unexpected error while adding product: {e}")
                messages.error(request, f"❌ Xatolik: {str(e)}")
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        form = ProductAdminForm()
    return render(request, 'store_admin/product_form.html', {'form': form, 'title': 'Mahsulot qo\'shish'})

@user_passes_test(is_admin, login_url='store_admin:login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductAdminForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                product = form.save()
                messages.success(request, f"✅ Mahsulot '{product.name}' muvaffaqiyatli yangilandi.")
                return redirect('store_admin:product_list')
            except IntegrityError as e:
                logger.error(f"IntegrityError while editing product: {e}")
                form.add_error('slug', "Slug allaqachon mavjud. Iltimos, boshqa slug kiriting.")
            except Exception as e:
                logger.error(f"Unexpected error while editing product: {e}")
                messages.error(request, f"❌ Xatolik: {str(e)}")
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        form = ProductAdminForm(instance=product)
    return render(request, 'store_admin/product_form.html', {'form': form, 'title': 'Mahsulotni tahrirlash'})

@user_passes_test(is_admin, login_url='store_admin:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('store_admin:product_list')
    return render(request, 'store_admin/product_confirm_delete.html', {'product': product})

@user_passes_test(is_admin, login_url='store_admin:login')
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store_admin/order_list.html', {'orders': orders})

@user_passes_test(is_admin, login_url='store_admin:login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store_admin/order_detail.html', {'order': order})

@user_passes_test(is_admin, login_url='store_admin:login')
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        old_status = order.status
        
        if new_status in dict(Order.STATUS_CHOICES) and new_status != old_status:
            # Handle Stock Update
            if new_status == 'confirmed':
                for item in order.items.all():
                    item.product.stock = max(0, item.product.stock - item.quantity)
                    item.product.save()
            elif new_status == 'cancelled' and old_status in ['confirmed', 'delivered']:
                for item in order.items.all():
                    item.product.stock += item.quantity
                    item.product.save()
            
            order.status = new_status
            order.save()
            messages.success(request, f"Buyurtma holati '{order.get_status_display()}' ga o'zgartirildi.")
    return redirect('store_admin:order_detail', pk=pk)

@user_passes_test(is_admin, login_url='store_admin:login')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store_admin/category_list.html', {'categories': categories})

@user_passes_test(is_admin, login_url='store_admin:login')
def category_add(request):
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya muvaffaqiyatli qo'shildi.")
            return redirect('store_admin:category_list')
    else:
        form = CategoryAdminForm()
    return render(request, 'store_admin/category_form.html', {'form': form, 'title': "Kategoriya qo'shish"})

@user_passes_test(is_admin, login_url='store_admin:login')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryAdminForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya yangilandi.")
            return redirect('store_admin:category_list')
    else:
        form = CategoryAdminForm(instance=category)
    return render(request, 'store_admin/category_form.html', {'form': form, 'title': "Kategoriyani tahrirlash"})

