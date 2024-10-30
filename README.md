# `KhataBook Admin` [`Dashboard`](https://adminkhatadashboard.pythonanywhere.com)

    unzip /home/adminkhatadashboard/app.zip
    find /home/adminkhatadashboard -type d -exec chmod 755 {} +
    
    pip install django-jazzmin
    python manage.py collectstatic
    zip -r project.zip .

![image](https://github.com/user-attachments/assets/6918584b-a8d8-4302-bad7-e72bc086ee01)
![image](https://github.com/user-attachments/assets/2428f8a6-cd50-45b9-9eee-7f40a07391e7)
![image](https://github.com/user-attachments/assets/46ae6127-bf4f-4ca6-8e06-d1460e8401d7)
![image](https://github.com/user-attachments/assets/bd90a8d9-c78d-4326-b97f-a42e10703e38)
![image](https://github.com/user-attachments/assets/e4f28df6-d67f-4411-a184-4e5ff2f493bd)

# settings.py
```py
INSTALLED_APPS = [
    'customers', # app name
    'jazzmin', # write it here

    'django.contrib.admin',
    ...
]

TIME_ZONE = 'Asia/Kolkata'
LOGIN_URL = '/login/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

# urls.py
```py
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

# admin.py
```py
from django.contrib import admin
from .models import Customer, Purchase
from django.db.models import Sum

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
    list_display = ('item_name', 'price', 'customer', 'purchase_date')
    list_filter = ('purchase_date', 'customer')  # Filters by date and customer
    search_fields = ('item_name', 'customer__name')  # Search by item and customer name

# Register the models with custom admin configurations
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Purchase, PurchaseAdmin)
```

