from django.contrib import admin
from .models import MenuItem, Cart, Order, OrderItem, Category


# Register your models here.
admin.site.register((MenuItem, Cart, Order, OrderItem, Category))
admin.autodiscover()