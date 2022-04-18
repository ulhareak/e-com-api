from django.contrib import admin

# Register your models here.

from .  import models

#admin.site.register(models.Category)
#admin.site.register(models.Product)
#admin.site.register(models.Place)
#admin.site.register(models.Restaurant)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' ,"name", "price" ,"image")

@admin.register(models.Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'title')
@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id',)
@admin.register(models.CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ('id',"cart","product",'price')

# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = 

# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = 