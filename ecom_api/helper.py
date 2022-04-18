
from django.core.mail import send_mail
from django.conf import settings
from .models import * 
from . serializers import ProductSerializer

def send_mail_to_user(instance , ids  ):
    subject = 'user products '
    message = f'Avdhut send email'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [instance.cart.user.email]
    send_mail(subject, message, email_from, recipient_list)
    return True

    