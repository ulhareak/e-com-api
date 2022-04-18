from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "%s " % self.title
    
    # @property
    # def category_set(self):
    #     return self.category_set.all()


class Product(models.Model):
    # def nameFile(instance, filename):
    #     return '/static/'.join(['images/products', str(instance.name), filename])
    category = models.ForeignKey(Category,related_name = 'products' ,   on_delete=models.CASCADE)
    name = models.CharField(unique = True ,max_length=50)
    price = models.IntegerField()
    image = models.ImageField( blank= True ,upload_to="images/products")

   
    def __str__(self):
        return "%s " % self.name


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    #total = models.IntegerField()

    def __str__(self):
        return "%s " % self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='product', on_delete=models.CASCADE)
    price = models.IntegerField()
