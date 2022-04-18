




from . import models 
from django.contrib.auth.models import User
from rest_framework import serializers 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','username','first_name' , 'last_name' ,
        'email',
         ]


class RegsterSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.User
        fields = ['username','first_name' , 'last_name' ,
        'password', 'email',
         ]
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        cart = models.Cart.objects.create(user = user)
        cart.save()
        return user

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
     class Meta :
         model= models.Product
         fields = ['id', "name","price" , "image"]

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many = True  )
    class Meta:
        model = models.Category 
        fields = ["id","title" , "products"]

    def create(self , validated_data):
        products = validated_data.pop("products")
        print(validated_data)
        cat  = models.Category.objects.create(**validated_data)
        print(type(cat))
        
        for  p in products :
            print(p)
            models.Product.objects.create( category = cat ,**p  )
        return cat

class CartItemSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ("cart", "product","price")

class CartItemsSerializerNew(serializers.ModelSerializer):
    cart = CartSerializer(many = False , read_only = True )
    product = ProductSerializer(many = False , read_only = True )
    total = serializers.SerializerMethodField()
    class Meta :
        model = models.CartItem
        fields = ( 'id' , "cart" , "product" ,"total")
    
    def get_total(self, instance):
        return instance.product.price 
    

