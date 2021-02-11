from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ImageAlbum(models.Model):
    name = models.CharField(max_length=255, null=False, default=False)

    def images(self):
        return Image.objects.filter(album=self.id)


class Image(models.Model):
    name = models.CharField(max_length=255, null=False, default=False)
    image = CloudinaryField("image", null=True, blank=True)
    default = models.BooleanField(default=False)
    album = models.ForeignKey(ImageAlbum, null=True, on_delete=models.CASCADE)


class Product(models.Model):
    shirt_sizes = [
        ("XS", "X-Small"),
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "X-Large"),
        ("XXL", "XX-Large"),
    ]
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null= False, blank=True)
    details= models.TextField(null=True, blank=True)
    item_type = models.CharField(max_length=50, null=False, default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    sizes = models.JSONField(default=list, null=True, blank=True)
    colors = models.JSONField(default=list, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    album = models.OneToOneField(ImageAlbum,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            url = ""
        return url

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    buyer_name = models.CharField(max_length=50)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class EmailRecipient(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class InfoRequester(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField(null=True)