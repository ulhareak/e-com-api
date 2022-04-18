#from distutils.log import Log
from django.shortcuts import render


from django.contrib.auth import login


from . import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import models
import json
# Authentication Classes
from knox.auth import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# Views Classes
from knox.views import LoginView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet , ViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView, CreateAPIView , ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# PAgination and Filter classes
from django_filters.rest_framework import DjangoFilterBackend
# views
from rest_framework.pagination import LimitOffsetPagination
# Custom Permissions 
from . permissions import CustomPermission
from . import helper

class ProductAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ CustomPermission] 

    def post( self , request , *args , **kwargs):
        ser = serializers.ProductSerializer(data = request.data)

        if ser.is_valid():
            ser.save()
            return Response("Products added successfully.")
        return Response(ser.errors)

class ProductAPIView(APIView):
    def post(self, request, *args, **kwargs):
        ser = None 
        if isinstance(request.data["category"] , dict):
            cat = serializers.CategorySerializer(data = request.data["category"])
            pro_list = None 
            if cat.is_valid():
                cat.save()
                cat  = (models.Category.objects.get(title =request.data["category"]["title"]))
                print(cat.id)
                pro_list =request.data['products'] 
                for p in pro_list:
                    p['category'] = cat.id
                print("pro list ",pro_list)
            ser = serializers.ProductSerializer(data=pro_list ,many=isinstance(pro_list, list) )
            print("avdhut1")
        else :
            ser = serializers.ProductSerializer(data=request.data )
        if ser.is_valid(raise_exception=True):
            ser.save()
            print("ak2")
            return Response({"response": 'Products added Successfully.'})


class CartItemModelViewset(ModelViewSet):
    #queryset = models.CartItem.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartItemsSerializerNew
 
    def get_queryset(self):
        cartitems = models.CartItem.objects.select_related("cart").filter(
            cart__user=self.request.user)
        
        return cartitems


class LoginView(LoginView):
    authentication_classes = [BasicAuthentication]


class LoginView(LoginView):
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        data = super(LoginView, self).post(request, format=None)
        data.data["user"] = serializers.UserSerializer(user).data
        return Response(data.data)


class CartItemAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = models.Cart.objects.get(user=request.user)
        cartitems = models.CartItem.objects.filter(cart=cart)
        ser = serializers.CartItemsSerializerNew(data=cartitems, many=True)
        if ser.is_valid():
            return Response(ser.data)
        sum_a = sum([item.product.price for item in cartitems])
        data = {"total": sum_a, "res": ser.data}
        return Response(data)

    def delete(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        ids = request.data["pid"] 
        print("ids", ids)
        print("type", type(ids))
        ids = list(ids)
        cart = models.Cart.objects.get(user=request.user)
        d = []
        for id in ids:
            product = models.Product.objects.get(id=id)
            c_item = models.CartItem.objects.create(
                cart=cart, product=product, price=product.price)
            
            c_item.save( )
            d.append(c_item)
        helper.send_mail_to_user(cart , ids)
       
        return Response({"msg": " product added to cart."})


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        ser = serializers.RegsterSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"response": 'User Created Successfully.'})


class CategoryList(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']


class ProductList(ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
