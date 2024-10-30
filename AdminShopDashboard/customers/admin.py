from django.contrib import admin
from .models import Customer, Purchase

class PurchaseInline(admin.TabularInline):
    model = Purchase
    extra = 1  # Number of extra blank forms

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Displays the name in the customer list
    inlines = [PurchaseInline]  # Shows purchases inline on the customer page

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'price', 'customer', 'purchase_date')
    list_filter = ('purchase_date', 'customer')  # Filters by date and customer
    search_fields = ('item_name', 'customer__name')  # Search by item and customer name

# Register the models with custom admin configurations
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Purchase, PurchaseAdmin)
