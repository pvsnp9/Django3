from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order, Customer, Product, Tag
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *

@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles= ['admin','staff'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles= ['admin','staff'])
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()

    customer_filter = OrderFilter(request.GET, queryset=orders)
    orders = customer_filter.qs

    context = {'customer': customer, 'orders': orders, 'total_orders':orders.count(), 'customer_filter':customer_filter}
    
    return render(request, 'accounts/customer.html', context)


# form to create orderss
@login_required(login_url='login')
@allowed_users(allowed_roles= ['admin','staff'])
def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        order_data = OrderForm(request.POST)
        if order_data.is_valid():
            order_data.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


# create multiple order for the customer
@login_required(login_url='login')
@allowed_users(allowed_roles= ['admin','staff'])
def createMultipleOrder(request, customer_key):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=customer_key)
    form = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        order_data = OrderFormSet(request.POST, instance=customer)
        if order_data.is_valid():
            order_data.save()
            return redirect('/')

    context = {'formset':form}
    return render(request, 'accounts/order_form.html', context)


# update order
@login_required(login_url='login')
@allowed_users(allowed_roles= ['admin','staff'])
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        order_data = OrderForm(request.POST, instance=order)
        if order_data.is_valid():
            order_data.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/single_order_form.html', context)


# remove order
@login_required(login_url='login')
@allowed_users(allowed_roles= ['admin','staff'])
def removeOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/remove_order.html', context)


# login 
@unauthenticated_user
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Please check your credentails')
    context = {}
    return render(request, 'accounts/login.html', context)


# Logout
def userLogout(request):
    logout(request)
    return redirect('login')

# user registrtion 
@unauthenticated_user
def registration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='customer'))
            messages.success(request, 'Account has been created for '+ form.cleaned_data.get('username'))
            return redirect('login')
    context = {'form':form, 'no-auth':True}
    return render(request, 'accounts/register.html', context)

# user page
def uesrPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)