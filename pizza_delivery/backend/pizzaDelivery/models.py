from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe


class PizzaBase(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return self.name

class PizzaSauce(models.Model):
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True, null=False)
    
    def __str__(self) -> str:
        return self.name

class PizzaCheese(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return self.name

class PizzaVeggie(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return self.name
   

class Pizza(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    decription = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    image = models.ImageField(upload_to='pizza_images/', null=True, blank=True)
    pizza_base = models.ForeignKey(PizzaBase, on_delete=models.PROTECT, related_name="pizza_b")
    pizza_sauce = models.ManyToManyField(PizzaSauce, related_name="pizza_s")
    pizza_cheese = models.ForeignKey(PizzaCheese, on_delete=models.PROTECT, related_name="pizza_c")
    pizza_veggie = models.ManyToManyField(PizzaVeggie, related_name="pizza_v")
    custom = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line1 = models.TextField()
    address_line2 = models.TextField()
    pincode = models.CharField(max_length=6, default="")
    city = models.CharField(max_length=255, null=True, default="")
    state = models.CharField(max_length=255, null=True, default="")
    country = models.CharField(max_length=255, null=True, default="")

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name
    

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("R", "Order Recieved"),
        ("I", "In the Kithen"),
        ("O", "Out for Delivery"),
        ("D", "Delevered")
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, null=True)
    payment_status = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.customer.user.first_name + ' ' + self.customer.user.last_name + ' ' + str(self.id)

class OrderItem(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    quantity = models.PositiveIntegerField(default=1)

