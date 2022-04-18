from rest_framework import permissions
from .models import *
from django.contrib.auth.models import User

class CustomPermission(permissions.BasePermission):
    """
    Global permission .
    """

    def has_permission(self, request, view):
        print("avdhut",request.user)
        user = User.objects.get(username = request.user)
        print("avinash",user.is_superuser)
        if request.method in ["POST", "GET"] and user.is_superuser == True:
            return True
        return False
