import random
from django.core.mail import send_mail
import secrets
from .models import EmailVerification
from django.utils import timezone
import os
from django.contrib.auth.models import Group

EMAIL = os.getenv("EMAIL_USER")

#this service is all for signUp.

def send_verification_email(email):
    #creating ramdom code because I can ._.
    code = str(random.randint(100000, 999999))



    obj, created = EmailVerification.objects.update_or_create(
        email=email,
        defaults={
            'code': code,
        }
    )

    #i have to make this pretier
    send_mail(
        "Your verification code",
        "Hello! This is your verification code:" + code + "it will expire after 5 minutes. Don't share it with anyone.",
        EMAIL,
        [email],
        fail_silently=False,
    )

def assign_client_group(user): 
    group, _ = Group.objects.get_or_create(name='Client') 
    user.groups.add(group)