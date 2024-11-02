from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Purchase
from .forms import CustomerForm, PurchaseForm
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Q, F, Case, When, DecimalField
from .forms import UserRegisterForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'customers/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('customer_list')  # Redirect to the main page
    else:
        form = AuthenticationForm()
    return render(request, 'customers/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # Associate customer with the logged-in user
            customer.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm()
    return render(request, 'customers/create_customer.html', {'form': form})

@login_required
def create_purchase(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.customer = customer
            purchase.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = PurchaseForm()
    return render(request, 'customers/create_purchase.html', {'form': form, 'customer': customer})

@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    purchases = customer.purchases.all()
    
    total_amount = purchases.aggregate(
        total=Sum(
            Case(
                When(is_payment=True, then=-F('price')),
                default=F('price'),
                output_field=DecimalField(),
            )
        )
    )['total']
    
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'purchases': purchases,
        'total_amount': total_amount or 0  # Default to 0 if no purchases
    })

@login_required
def customer_list(request):
    customers = Customer.objects.filter(user=request.user)
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def purchase_list_ajax(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    purchases = customer.purchases.all()
    
    # Sorting
    sort_field = request.GET.get('sort', 'item_name')
    sort_direction = request.GET.get('direction', 'asc')
    if sort_direction == 'desc':
        sort_field = f'-{sort_field}'
    purchases = purchases.order_by(sort_field)
    
    # Search filter
    search_query = request.GET.get('search', '')
    if search_query:
        purchases = purchases.filter(
            Q(item_name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(purchases, 5)  # Show 5 purchases per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Calculate total amount considering is_payment status
    total_amount = purchases.aggregate(
        total=Sum(
            Case(
                When(is_payment=True, then=-F('price')),
                default=F('price'),
                output_field=DecimalField(),
            )
        )
    )['total'] or 0

    # Serialize data for JSON response
    purchases_data = [
        {
            'item_name': purchase.item_name,
            'price': float(purchase.price),
            'purchase_date': purchase.purchase_date.strftime('%b. %d, %Y, %I:%M %p')
        }
        for purchase in page_obj
    ]

    return JsonResponse({
        'purchases': purchases_data,
        'total_amount': total_amount,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
    })

@login_required
def customer_list_ajax(request):
    search_query = request.GET.get('search', '')
    sort_field = request.GET.get('sort', 'id')
    sort_direction = request.GET.get('direction', 'asc')
    page_number = request.GET.get('page', 1)

    # Sorting
    if sort_direction == 'desc':
        sort_field = f'-{sort_field}'

    customers = Customer.objects.filter(name__icontains=search_query, user=request.user).order_by(sort_field)

    # Pagination
    paginator = Paginator(customers, 5)  # Show 5 customers per page
    page_obj = paginator.get_page(page_number)

    # Serialize customer data
    customers_data = [
        {
            'id': customer.id,
            'name': customer.name,
            'profile_photo': customer.profile_photo.url if customer.profile_photo else '',
            'detail_url': reverse('customer_detail', args=[customer.id])
        }
        for customer in page_obj
    ]

    return JsonResponse({
        'customers': customers_data,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
    })
