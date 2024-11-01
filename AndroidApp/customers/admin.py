# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Purchase
from django.db.models import Sum
from django.db.models import Sum, Case, When, F, DecimalField

class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1
    can_delete = False

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_amount_spent', 'latest_purchase_date', 'customer_id')
    search_fields = ('name', 'id')
    list_filter = ('purchases__purchase_date',)
    inlines = [PurchaseInline]
    readonly_fields = ('photo_tag',)

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 150px; height: auto;" />', obj.photo.url)
        return "No Image"

    photo_tag.short_description = 'Display Photo'

    def customer_id(self, obj):
        return obj.id

    customer_id.short_description = 'Customer ID'

    def latest_purchase_date(self, obj):
        latest_purchase = obj.purchases.order_by('-purchase_date').first()
        return latest_purchase.purchase_date if latest_purchase else "No purchases"

    def total_amount_spent(self, obj):
        total = obj.purchases.aggregate(
            total=Sum(
                Case(
                    When(is_payment=True, then=-F('price')),
                    default=F('price'),
                    output_field=DecimalField()
                )
            )
        )['total']
        return total if total else 0

    latest_purchase_date.short_description = 'Latest Purchase Date'
    total_amount_spent.short_description = 'Total Amount Spent'

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'paid_status', 'customer', 'purchase_date')
    list_filter = ('purchase_date', 'customer', 'is_payment')
    search_fields = ('item_name', 'customer__name')

    fieldsets = (
        ('Purchase Information', {
            'fields': ('customer', 'item_name', 'price')
        }),
        ('Payment Status', {
            'fields': ('is_payment',),
        }),
    )

    def paid_status(self, obj):
        if obj.is_payment:
            return format_html('<span style="color: green;">Paid</span>')
        else:
            return format_html('<span style="color: red;">-</span>')

    paid_status.short_description = 'Status'

# Register the models with custom admin configurations
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Purchase, PurchaseAdmin)