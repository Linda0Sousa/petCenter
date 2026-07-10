from datetime import timedelta
import random
from django.core.mail import send_mail
import secrets
from .models import EmailVerification, User
from django.utils import timezone
import os
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

EMAIL = os.getenv("EMAIL_USER")

#this service is all for signUp.

def send_verification_email(email):
    #creating random code because I can ._.
    code = str(random.randint(100000, 999999))

    obj, created = EmailVerification.objects.update_or_create(
        email=email,
        defaults={
            'code': code,
        }
    )

    #i have to make this pretty
    send_mail(
        "Your verification code",
        "Hello! This is your verification code:" + code + "it will expire after 5 minutes. Don't share it with anyone.",
        EMAIL,
        [email],
        fail_silently=False,
    )

#puts the user to client automatically
def assign_client_group(user): 
    group, _ = Group.objects.get_or_create(name='Client') 
    user.groups.add(group)

#in here is made email verification and is where user is activated
def verify_code(request, email):
    user = get_object_or_404(User, email=email)

    if request.method == 'GET':
        verification = EmailVerification.objects.filter(email=email).first()

        if verification and timezone.now() - verification.created_at < timedelta(seconds=30):
            pass
        else:
            send_verification_email(email)

    if request.method == 'POST':
        input_code = request.POST.get('code', '').strip()

        verification = EmailVerification.objects.filter(email=email).first()

        if not verification:
            return False, "Email was not found, please try again"

        # Expiration 
        if timezone.now() - verification.created_at > timedelta(minutes=5):
            verification.delete()
            return False, "Code expired, please try again"

        # Code check
        if input_code == verification.code:
            user.is_active = True
            user.save()
            verification.delete()
            return True, "Verification successful"
        else:
            return False, "Wrong code"