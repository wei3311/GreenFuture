import requests
import json
from django.shortcuts import redirect, render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#Create home View
def home(request):
    context = {}

    #Return HttpResponse object of the template (home.html) rendered with given context
    return render(request, 'store/home.html', context)  

#Create register View
def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')  #retrived firstname from HTML form
        lastname = request.POST.get('lastname')    #retrived lastname from HTML form
        username = request.POST.get('username')    #retrived username from HTML form
        email = request.POST.get('email')          #retrived email from HTML form
        password = request.POST.get('password')    #retrived password from HTML form

        #Create & Save the User object into database
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=firstname, last_name=lastname)

        #Create & Save the Customer object into database at the same time
        Customer.objects.create(user=user, name=username, email=email)

        user.save()

        print('User Created')

        #Redirect user to Login webpage after registration
        return redirect('/accounts/login')

    else:
        #Load the template (Register.html) and return HttpResponse
        return render(request, 'store/register.html')


def login(request):
    if request.method == 'POST':
        form = authenticate(request=request, data=request.POST)         #Verify the requests
        if form.is_valid():
            username = form.cleaned_data.get('username')                #Cleaned & Validated username data 
            password = form.cleaned_data.get('password')                #Cleaned & Validated password data
            user = authenticate(username=username, password=password)   #Verify a username & password
            if user is not None:                                        #If user exist, redirect to Store webpage
                login(request, user)
                return redirect('/')

    context = {'form': form}
    #Return HttpResponse object of the template (login.html) rendered with given context
    return render(request, "store/login.html", context)


def inquiry(request):
    if request.method == 'POST':
        #Googel ReCAPTCHA methods
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LfCoGAdAAAAAFlA8KTsV8l_3iSULp7lFGYI2fjr"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)

        #If the ReCAPTCHA is failed, redirect to inquiry section again and show error message
        if cap_json['success'] == False:
            messages.error(request, 'Invalid Captcha Try Again.')
            return redirect('/#inquiry')

        emailAddress = request.POST.get('input_email_inquiry')  #retrived input_email_inquiry from HTML form
        title = request.POST.get('input_title_inquiry')         #retrived input_title_inquiry from HTML form
        fullName = request.POST.get('input_name_inquiry')       #retrived input_name_inquiry from HTML form
        phoneNo = request.POST.get('input_phoneNo_inquiry')     #retrived input_phoneNo_inquiry from HTML form
        inquiry = request.POST.get('input_inquiry')             #retrived input_inquiry from HTML form

        #Create & Save the User object into database and show success message
        inquiry = Inquiry.objects.get_or_create(
            emailAddress=emailAddress, title=title, fullName=fullName, phoneNo=phoneNo, inquiry=inquiry)
        messages.success(request, 'Contact request submitted successfully.')
        print('Inquiry Created')

        return redirect('/#inquiry')


@login_required  #Only authorized account can access Store view.
def store(request):
    #Define the user identification
    customer = request.user.customer         
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    #Retrive the Product data from database
    products = Product.objects.all()

    #Mapping template variable "products" to products
    context = {'products': products}

    #Return HttpResponse object of the template (store.html) rendered with given context
    return render(request, 'store/store.html', context)


def cart(request):
    #Define the user identification
    customer = request.user.customer

    #Get Order into database
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    #Retrive the OrderItem data from database
    items = order.orderitem_set.all()

    #Mapping template variable "items" to items and "order" to order
    context = {'items': items, 'order': order}

    #Return HttpResponse object of the template (cart.html) rendered with given context
    return render(request, 'store/cart.html', context)


def productSearch(request):
    if request.method == "GET":
        #Filter the product with entered query(q) in template search bar
        results = Product.objects.filter(name__icontains=request.GET.get('q'))

        #Mapping template variable "results" to results
        context = {"results": results}

        #Return HttpResponse object of the template (productSearch.html) rendered with given context
        return render(request, 'store/productSearch.html', context)

    return render(request, 'store/productSearch.html')


def checkout(request):
    #Define the user identification
    customer = request.user.customer
    
    #Get Order into database
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #Retrive the OrderItem data from database
    items = order.orderitem_set.all()

    #Mapping template variable "items" to items & "order" to order
    context = {'items': items, 'order': order}
    total = order.get_cart_total

    if request.method == 'POST':

        receiver = request.POST.get('receiver')     #retrived receiver from HTML form
        contactNo = request.POST.get('contactNo')   #retrived contactNo from HTML form
        address = request.POST.get('address')       #retrived address from HTML form
        city = request.POST.get('city')             #retrived city from HTML form
        state = request.POST.get('state')           #retrived state from HTML form
        zipcode = request.POST.get('zipcode')       #retrived zipcode from HTML form

        #Create & Save the ShippingAddress object into database
        ShippingAddress.objects.get_or_create(customer=customer, order=order, receiver=receiver, contactNo=contactNo, address=address,
                                              city=city, state=state, zipcode=zipcode, total=total)

        print('Shipping Address is Created')

        #Redirect user to Store webpage after registration
        return redirect('/store')

    else:
        return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)     #Get the data from JavaScript (cart.js) object of the data
    productId = data['productId']       #Get the productID data from cart.js
    action = data['action']             #Get the action data from cart.js

    print('Action:', action)
    print('productId:', productId)

    #Define the user identification
    customer = request.user.customer
    product = Product.objects.get(id=productId)  #Get the ProductID of product which involve in changes

    #Save the changes of Order object into database
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #Save the changes of OrderItem object into database
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':         
        orderItem.quantity = (orderItem.quantity + 1)  #add = Quantity +1
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)  #remove = Quantity -1
    elif action == 'delete':
        orderItem.quantity = 0                         #delete = Quantity =0

    #Save the changes of orderItem into database
    orderItem.save()

    #If the quantity is zero or below zero, delete the product from Cart list
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
