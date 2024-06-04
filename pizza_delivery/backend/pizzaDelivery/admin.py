from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

@admin.register(models.Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name','incredients', 'price', 'custom', 'image_tag']
    autocomplete_fields = ['pizza_base', 'pizza_sauce', 'pizza_cheese', 'pizza_veggie']
    search_fields = ['name']
    list_select_related = ['pizza_base', 'pizza_cheese']
    list_filter = ['custom']

    def image_tag(self, obj):
        try:
            return format_html('<img src="{}" alt="pizza image" style="max-width:100px; max-height:100px"/>'.format(obj.image.url))
        except ValueError as e:
            return format_html('<img src="" alt="pizza image" style="max-width:200px; max-height:200px"/>')

    image_tag.short_description = 'Image'

    def incredients(self, pizza):
        desc = "<b>Base : </b>" +str(pizza.pizza_base) + "</br><b>Sauces: </b>  "
        
        sauces = pizza.pizza_sauce.all()
        for sauce in sauces:
            desc += str(sauce.name) + ", "
        desc = desc[0:-2]
        
        desc += "</br><b>Veggies: </b>  "
        veggies = pizza.pizza_veggie.all()
        for veggie in veggies:
            desc += str(veggie) + ", "
        desc = desc[0:-2]
        
        desc += "</br><b>Cheese: </b>  "
        desc += str(pizza.pizza_cheese)

        return format_html(desc)

@admin.register(models.PizzaBase)
class PizzaItemsAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']
    search_fields = ['name']

@admin.register(models.PizzaCheese)
class PizzaItemsAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']
    search_fields = ['name']

@admin.register(models.PizzaSauce)
class PizzaItemsAdmin(admin.ModelAdmin):
    list_display = ['name','is_available']
    search_fields = ['name']

@admin.register(models.PizzaVeggie)
class PizzaItemsAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']
    search_fields = ['name']

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', "address"]
    search_fields = ['user']

    @admin.display()
    def address(self, customer):
        return f'{customer.address_line1}, {customer.address_line2}, {customer.city}, {customer.state}, {customer.pincode}'
    
    @admin.display(ordering="user")
    def name(self, customer):
        return customer.user

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_status', 'order_items', 'customer', 'customer_address' ,'order_status']
    search_fields = ['customer']
    autocomplete_fields = ['customer']
    list_editable = ['order_status']

    @admin.display()
    def order_items(self, order):
        url =(
            reverse("admin:pizzaDelivery_orderitem_changelist")
            + "?"
            + urlencode({
                "order_id":str(order.id)
            })
        )
        return format_html(f'<a href="{url}">{order.items}</a>') 
    
    def customer_address(self, order):
        return f'{order.customer.address_line1}, {order.customer.address_line2}, {order.customer.city}, {order.customer.state}, {order.customer.pincode}'

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related('orderitems').annotate(items = Count("orderitems"))

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['pizza', 'quantity']
    autocomplete_fields = ['pizza', 'order']
