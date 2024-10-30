from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Purchase
from .forms import CustomerForm, PurchaseForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def redirect_to_admin(request):
    return redirect('/admin')

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm()
    return render(request, 'customers/create_customer.html', {'form': form})

@login_required
def create_purchase(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
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
    customer = get_object_or_404(Customer, id=customer_id)
    purchases = customer.purchases.all()
    total_amount = purchases.aggregate(Sum('price'))['price__sum']
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'purchases': purchases,
        'total_amount': total_amount
    })

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})
