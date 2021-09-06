
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import serializers

from .forms import OrderForm, ProductForm, RegisterForm, CustomerForm, UserupdateForm, ProfileUdateForm
from .filters import customerfilter #, productfilter,totalorderfilter
from .models import *

from .decorators import unauthenticated_user
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from datetime import date, timedelta


# Create your views here.
 

######## user views

@unauthenticated_user
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Welcome "{user}" Your Acount Was Created ! Now Login Please ')
            return redirect('login')
    contxt = {
        'form':form,
        'title':'Register',
        }
    return render(request,'acounts/register.html',contxt)


@unauthenticated_user        
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Your account is disabled!")
                return redirect('login')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {
        'title':'Login',
    }
    return render(request, 'acounts/login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def userpage(request):
    user = request.user# User.objects.get(id=id)
    pic = user.profile.profile_pic.url
    u_form = UserupdateForm(instance=user)
    p_form = ProfileUdateForm(instance=user.profile)
    if request.method == 'POST':
        u_form = UserupdateForm(request.POST, instance=user)
        p_form = ProfileUdateForm(request.POST,request.FILES,  instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request,'Your Acount was Updated')
            u_form.save()
            p_form.save()
    contxt = {
        'pic':pic,
        'user':user,
        'u_form':u_form,
        'p_form':p_form,
        'title':user.username,
    }
    return render(request, 'acounts/user_page.html', contxt)



####### dashbord view

@login_required(login_url='login')
def home(request):
    user = get_object_or_404(User,username=request.user.username)


    #################
    # get all orders for user
    ordersall = Order.objects.none()[:6]
    for customer in user.customer_set.all():
        for order in customer.order_set.all():

            ordersall |= Order.objects.filter(id=order.id).order_by('-date_created')


    ######################

    # get last 6 orders 
    orders = ordersall[:6] 
    
    order_today = None
    order_last_30day =None
    mony_today =None
    mony_last_30day=None

    ###################
    # get count of order today
    if ordersall:
        startdate_today = date.today()
        enddate_today = startdate_today + timedelta(days=1)
        order_today = ordersall.filter(date_created__range=[startdate_today,enddate_today])

        ####################
        # get count of order last 30
        day_now = date.today()
        startdate_30 = day_now + timedelta(days=1)
        enddate_30 = startdate_30 - timedelta(days=30)
        order_last_30day = ordersall.filter(date_created__range=[enddate_30,startdate_30])

        ###################

        # get count of all mony order today

        mony_today = 0
        for order in order_today:
            mony_today += order.product.price
        
        ###################

        # get count of all mony order last 30 days

        mony_last_30day = 0
        for order in order_last_30day:
            mony_last_30day += order.product.price
    ##################
    

    ##################
    # get best 6 customers (filter by count of orders)

    customersall = request.user.customer_set.all()
    customers = sorted(customersall,key= lambda x: x.order_set.all().count(), reverse=True)[:6]

    
  
    ###################

    # filrer 
    myfilters = customerfilter(request.GET,queryset=customersall)
    customersall = myfilters.qs




    contxt = {
 
        'customers':customers,
        'orders':orders,
        'myfilters':myfilters,
        'order_today':order_today,
        'order_last_30day':order_last_30day,
        'mony_today':mony_today,
        'mony_last_30day':mony_last_30day,
        'title':'Dashboard',
    }

    return render(request, 'acounts/dashboard.html',contxt)






####### customers views

@login_required(login_url='login')
def customer(request,id):
    user = request.user
    customer = get_object_or_404(Customer, id=id, user=user)# Customer.objects.get(id=id)
    orders = customer.order_set.all().order_by('-date_created')
    total_order = orders.count()

    startdate = date.today()
    enddate = startdate + timedelta(days=1)
    order_today = customer.order_set.all().filter(date_created__range=[startdate,enddate])

    mony_total = 0
    mony_today = 0

    for order in orders:
        mony_total += order.product.price 

    for order in order_today:
        mony_today += order.product.price 
     



    contxt ={
        'customer':customer,
        'orders':orders,
        'total_order':total_order,
        'order_today':order_today,
        'mony_today':mony_today,
        'mony_total':mony_total,
        'title':customer.name,
    }

    return render(request, 'acounts/customer.html',contxt)


@login_required(login_url='login')
def customerspage(request):
    customers = request.user.customer_set.all().order_by('-date_created')


    contxt = {
        'customers':customers,
        'title':'Customers',
    }
    return render(request,'acounts/customers_page.html',contxt)


@login_required(login_url='login')
def createcustomer(request):

    user = request.user
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers_page')
    contxt = {
        'form':form,
        'user':user,
        'butoon':'Create',
        'action':'Create New Customer :',
        'title':'Create Customer',
    }
    return render(request, 'acounts/customer_form.html', contxt)


@login_required(login_url='login')
def updatecustomer(request,id):
    user = request.user
    customer = get_object_or_404(Customer,id=id, user=user)# .objects.get(id=id)
    c_name = customer.name
    c_email = customer.email
    c_phone = customer.phone
    c_adress = customer.adress
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            messages.success(request,'Customer info was Updated')
            form.save()
            return HttpResponseRedirect(f"/customer/{customer.id}")
            
    contxt = {
        'form':form,
        'user':user,
        'c_name':c_name,
        'c_email':c_email,
        'c_phone':c_phone,
        'c_adress':c_adress,
        'customer':customer,
        'butoon':'Update',
        'action':'Update The Customer :',
        'title':f'Update {customer.name}',
    }
    return render(request, 'acounts/customer_form.html', contxt)


@login_required(login_url='login')
def deletecustomer(request,id):
    user=request.user
    customer = get_object_or_404(Customer,id=id, user=user)# Customer.objects.get(id=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers_page')
    contxt = {
        'customer':customer,
        'title':f'Delete {customer.name}',
    }
    return render(request,'acounts/delete_customer.html',contxt)







######## orders views

@login_required(login_url='login')
def createorder(request,id):
    user = get_object_or_404(User,username=request.user.username)
    customers = get_list_or_404(Customer,user=user)
    products = get_list_or_404(Product,user=user)
    customerin = get_object_or_404(Customer,id=id,user=user) 
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('totalorder')

    contxt = {
        'form':form,
        'customerin':customerin,
        'customers':customers,
        'products':products,
        #'statuses':statuses,
        'action':'Creating Order...',
        'button':'Create',
        'title':'Create order',
    }
    return render(request, 'acounts/order_form.html',contxt)



@login_required(login_url='login')
def updateorder(request,id):
    user = get_object_or_404(User,username=request.user.username)
    order = get_object_or_404(Order,id=id,customer__user=user)
    customers = get_list_or_404(Customer,user=user)
    products = get_list_or_404(Product,user=user)

    customerin = order.customer
    productin = order.product
    statusin = order.status
    notin = order.note
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')


    contxt = {
        'customers':customers,
        'products':products,
        'form':form,
        'customerin':customerin,
        'productin':productin,
        'statusin':statusin,
        'notin':notin,
        'action':'Update Order...',
        'button':'Update',
        'title':f'Update order - {order}',
    }
    return render(request, 'acounts/order_form.html',contxt)


@login_required(login_url='login')
def deleteorder(request,id):
    user=request.user
    order = get_object_or_404(Order,id=id,customer__user=user) 
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    contxt = {
        'order':order,
        'title':f'Delete order - {order}',
        }
    return render(request, 'acounts/delete_order.html',contxt)


@login_required(login_url='login')
def totalorder(request):
    user = get_object_or_404(User,username=request.user.username)
    customers = Customer.objects.filter(user=user)
    products = Product.objects.filter(user=user)
    orders = Order.objects.none()
    for customer in user.customer_set.all():
        for order in customer.order_set.all():
            orders |= Order.objects.filter(pk=order.pk).order_by('-date_created')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()
    outfordelivery = orders.filter(status='Out for delivery').count()



    contxt = {
        'customers':customers,
        'products':products,
        'orders':orders,
        #'myfilters':myfilters,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'outfordelivery':outfordelivery,
        'title':'Total order',

    }
    return render(request, 'acounts/total_order.html',contxt)








####### product views

@login_required(login_url='login')
def products(request):

    
    products = request.user.product_set.all().order_by('-date_created')

    contxt = {
        'products':products,
        'title':'Products',
    }

    return render(request, 'acounts/products.html',contxt)


@login_required(login_url='login')
def createproduct(request):
    user = get_object_or_404(User,username=request.user.username) 
    form = ProductForm(initial={'user':user})
    if request.method == 'POST':
        form = ProductForm(request.POST,initial={'user':user})
        if form.is_valid():
            form.save()
            return redirect('products')

    contxt = {
        'form':form,
        'action':'Creating Product...',
        'button':'Create',
        'title':'Create Product',
    }
    return render(request, 'acounts/product_form.html',contxt)


@login_required(login_url='login')
def updateproduct(request,id):
    user=request.user
    product = get_object_or_404(Product,id=id,user=user) 

    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    contxt = {
        'form':form,
        'action':'Update Product...',
        'button':'Update',
        'title':f'Update {product}',
    }
    return render(request, 'acounts/product_form.html',contxt)


@login_required(login_url='login')
def deleteproduct(request,id):
    user=request.user
    product = get_object_or_404(Product,id=id,user=user) 
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    contxt = {
        'product':product,
        'title':f'Delete {product}',
        }
    return render(request, 'acounts/delete_product.html',contxt)



################################
################################

