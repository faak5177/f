from django.contrib import admin
from .models import Role, User, Category, Manufacturer, Supplier, Product, PickPoint, Order

for m in (Role, User, Category, Manufacturer, Supplier, Product, PickPoint, Order):
    admin.site.register(m)
