from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.template.response import TemplateResponse

class CustomAdminSite(AdminSite):
    site_header = "TechShop Administration"
    site_title = "TechShop Admin Portal"
    index_title = "Welcome to TechShop Portal"

    def index(self, request, extra_context=None):
        from apps.orders.models import Order
        
        # Calculate dashboard metrics
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today_start - timedelta(days=today_start.weekday())
        
        total_orders = Order.objects.count()
        today_orders = Order.objects.filter(created_at__gte=today_start).count()
        week_orders = Order.objects.filter(created_at__gte=week_start).count()
        total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        recent_orders = Order.objects.order_by('-created_at')[:5]

        extra_context = extra_context or {}
        extra_context['custom_dashboard'] = {
            'total_orders': total_orders,
            'today_orders': today_orders,
            'week_orders': week_orders,
            'total_revenue': total_revenue,
            'recent_orders': recent_orders,
        }
        
        return super().index(request, extra_context=extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')
