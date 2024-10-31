from django.contrib import admin
from .models import Customer, Purchase
from django.db.models import Sum
from django.utils.html import format_html

class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1  # Number of extra blank forms

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_amount_spent', 'latest_purchase_date', 'customer_id')  # Added customer ID as a new column
    search_fields = ('name', 'id')  # Enable search by customer name
    list_filter = ('purchases__purchase_date',)  # Enable filtering by purchase date
    inlines = [PurchaseInline]

    def customer_id(self, obj):
        return obj.id  # Returns the customer ID

    customer_id.short_description = 'Customer ID'  # Column name in the admin interface

    def latest_purchase_date(self, obj):
        latest_purchase = obj.purchases.order_by('-purchase_date').first()
        return latest_purchase.purchase_date if latest_purchase else "No purchases"

    def total_amount_spent(self, obj):
        total = obj.purchases.aggregate(total=Sum('price'))['total']
        return total if total else 0

    latest_purchase_date.short_description = 'Latest Purchase Date'
    total_amount_spent.short_description = 'Total Amount Spent'

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'paid_status', 'customer', 'purchase_date')
    list_filter = ('purchase_date', 'customer')
    search_fields = ('item_name', 'customer__name')

    def paid_status(self, obj):
        if obj.price < 0:
            return format_html('<span style="color: green;">Paid</span>')
        else:
            return format_html('<span style="color: red;">-</span>')

    paid_status.short_description = 'Status'  # Column name in the admin interface

# Register the models with custom admin configurations
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Purchase, PurchaseAdmin)
