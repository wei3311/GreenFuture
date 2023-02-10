from django.db import models
from django.contrib.auth.models import User

#Create Customer class
class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#Create Product class
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    desc = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images')  #The uploaded image will be saved into "images" folder
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    #@property is a decorator for method in the class that get value in method, it make usage of getter and setter easier
    @property  
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

#Create Order class
class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return 'OrderID: %s' % (self.id)

    #Calculate the total amount of the product(s) in cart
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    #Sum up the quantity of the product(s) in cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

#Create OrderItem class
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - (%s) - %s' % (self.id, self.order, self.product)

    #Calculate the total amount of EACH OF the product(s) in cart
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

#Create ShippingAddress class
class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    receiver = models.CharField(max_length=200, null=False)
    contactNo = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    total = models.FloatField()

    def __str__(self):
        return '%s - %s' % (self.receiver, self.order)

#Create Inquiry class
class Inquiry(models.Model):
    emailAddress = models.CharField(max_length=200, null=False)
    title = models.CharField(max_length=200, null=False)
    complete = models.BooleanField(default=False)
    fullName = models.CharField(max_length=200, null=False)
    phoneNo = models.CharField(max_length=200, null=False)
    inquiry = models.TextField(max_length=200, null=False)

    def __str__(self):
        return self.emailAddress
