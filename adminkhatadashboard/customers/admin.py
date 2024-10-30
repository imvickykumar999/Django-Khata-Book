from django.contrib import admin
from .models import Customer, Purchase
from django.db.models import Sum
from django.utils.html import format_html

class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1  # Number of extra blank forms

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'latest_purchase_date', 'total_amount_spent')  # Display total amount spent
    inlines = [PurchaseInline]  # Shows purchases inline on the customer page

    def latest_purchase_date(self, obj):
        latest_purchase = obj.purchases.order_by('-purchase_date').first()  # Get the latest purchase by date
        return latest_purchase.purchase_date if latest_purchase else "No purchases"

    def total_amount_spent(self, obj):
        total = obj.purchases.aggregate(total=Sum('price'))['total']
        return total if total else 0

    latest_purchase_date.short_description = 'Latest Purchase Date'  # Column name in the admin interface
    total_amount_spent.short_description = 'Total Amount Spent'  # Column name for total amount

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'paid_status', 'customer', 'purchase_date')
    list_filter = ('purchase_date', 'customer')
    search_fields = ('item_name', 'customer__name')

    def paid_status(self, obj):
        if obj.price < 0:
            return format_html('<span style="color: red;">Paid</span>')
        return ""

    paid_status.short_description = 'Status'  # Column name in the admin interface

# Register the models with custom admin configurations
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Purchase, PurchaseAdmin)
