from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    context = {
            'orders': orders,
            'customers': customers,
            'total_orders': orders.count(),
            'delivered': orders.filter(status='Delivered').count(),
            'pending':orders.filter(status='Pending').count()
        }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})


def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    context = {'customer': customer, 'orders': orders, 'total_orders':orders.count()}
    
    return render(request, 'accounts/customer.html', context)