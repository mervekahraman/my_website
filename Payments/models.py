from django.db import models
from django.contrib.auth.models import User
from Shop.models import Product
from django.db.models.signals import post_save
class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=200,blank=True)
    address = models.CharField(max_length=255,blank=True)
    province = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.pk)}'

def create_shipping_address(sender,instance,created,**kwargs):
    if created:
        user_ship = ShippingAddress(user=instance)
        user_ship.save()
post_save.connect(create_shipping_address,sender=User)



class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=200)
    shippingaddress = models.TextField(max_length=255)
    money = models.DecimalField(decimal_places=2,max_digits=7)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order - {str(self.pk)}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    customer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    price = models.DecimalField(max_digits=7,decimal_places=5)

    def __str__(self):
        return f'OrderItem - {str(self.pk)}'