from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    new_date = models.DateField(auto_now=True)
    phone = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=200,blank=True)
    province = models.CharField(max_length=200,blank=True)
    district = models.CharField(max_length=200,blank=True)
    zipcode = models.CharField(max_length=200,blank=True)
    old_cart_values = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile,sender=User)


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     shippingaddress = models.OneToOneField(Address, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.customer) + " @ " + str(self.shippingaddress)
#

class Product(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=5)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    description_product = models.CharField(max_length=250, default="",blank= True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    is_Sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=5)

    def __str__(self):
        return self.name



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=50, default="",blank=True)
    phone = models.CharField(max_length=20, default="",blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)

