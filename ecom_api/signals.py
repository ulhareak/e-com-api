from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from .helper import *
 
 
@receiver(post_save, sender=CartItem)
def cartitem_added(sender, instance, created, **kwargs):
    print("inside signals ")
    print( "sender",sender)
    print("instance",instance)
    print("created",created)
    print(instance.cart.user.email)
    if created:
        print("avdhut added")
        send_mail_to_user(instance )
