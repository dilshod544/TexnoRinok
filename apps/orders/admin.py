from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product_name', 'price', 'quantity', 'subtotal']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'city', 'status', 'total_price', 'created_at']
    list_filter = ['status', ('created_at', admin.DateFieldListFilter), 'city']
    list_editable = ['status']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    date_hierarchy = 'created_at'
    actions = ['mark_confirmed', 'mark_shipped', 'export_to_csv']

    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = "Customer Name"

    @admin.action(description='Mark selected as confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Mark selected as shipped')
    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Customer', 'Phone', 'City', 'Status', 'Total Price', 'Date'])
        for order in queryset:
            writer.writerow([order.id, f"{order.first_name} {order.last_name}", order.phone, order.city, order.status, order.total_price, order.created_at])
        return response
