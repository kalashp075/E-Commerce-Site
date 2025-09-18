from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    birthdate = models.DateField()

    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    brand = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    available_quantity = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail')
    strap_material = models.CharField(max_length=100, default="Stainless Steel")
    glass_material = models.CharField(max_length=100, default="Sapphire")
    strap_color = models.CharField(max_length=100, default="fill")
    dial_color = models.CharField(max_length=50, default="fill")
    case_thickness = models.CharField(max_length=100, blank=True, null=True)  
    warranty = models.CharField(max_length=100, blank=True, null=True, default="2 Years")
    frame_shape = models.CharField(max_length=50, default="Round")  
    water_resistance = models.CharField(max_length=50, default="3 ATM")  

    def __str__(self):
        return f"Details for {self.product.name}"

