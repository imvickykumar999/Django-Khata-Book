from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_customer, name='create_customer'),
    path('<int:customer_id>/purchase/', views.create_purchase, name='create_purchase'),
    path('<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('', views.customer_list, name='customer_list'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('customers/<int:customer_id>/purchases/', views.purchase_list_ajax, name='purchase_list_ajax'),
    path('customers/ajax/', views.customer_list_ajax, name='customer_list_ajax'),
]
