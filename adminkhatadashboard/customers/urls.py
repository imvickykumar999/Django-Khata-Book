from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_customer, name='create_customer'),
    path('<int:customer_id>/purchase/', views.create_purchase, name='create_purchase'),
    path('<int:customer_id>/', views.customer_detail, name='customer_detail'),
    #path('all/', views.customer_list, name='customer_list'),
    path('', views.redirect_to_admin),
]
