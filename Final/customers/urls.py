from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_customer, name='create_customer'),
    path('<int:customer_id>/purchase/', views.create_purchase, name='create_purchase'),
    path('<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('', views.customer_list, name='customer_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
