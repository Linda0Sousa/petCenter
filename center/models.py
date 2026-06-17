from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import phonenumbers
from phonenumbers import format_number, PhoneNumberFormat
from django.core.validators import validate_email

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    #email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email")
        ]

    def clean(self):
        super().clean()

        errors = {}

        if not self.email:
            errors["email"] = "Email é obrigatório"

        try:
            validate_email(self.email)
        except ValidationError:
            errors["email"] = "Email invalido"

        if self.phone_number:
            try:
                number = phonenumbers.parse(self.phone_number, "PT")
            except phonenumbers.NumberParseException:
                errors["phone_number"] = "Número inválido"

            if not phonenumbers.is_valid_number(number):
                errors["phone_number"] = "Número inválido"

        if errors:
            raise ValidationError(errors)

        def save(self, *args, **kwargs):
            if self.phone_number:
                number = phonenumbers.parse(self.phone_number, "PT")
                self.phone_number = format_number(number, PhoneNumberFormat.E164)

            self.full_clean()
            super().save(*args, **kwargs)

class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Status(models.Model):
    class StatusChoices(models.TextChoices):
        DEAD = 'dead', 'Dead'
        UNAVAILABLE = 'unavailable', 'Unavailable'
        AVAILABLE = 'available', 'Available'
        ADOPTED = 'adopted', 'Adopted'

    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.UNAVAILABLE,
        null=False,
    )

class Pet(models.Model):
    class StatusChoices(models.TextChoices):
        DEAD = 'dead', 'Dead'
        UNAVAILABLE = 'unavailable', 'Unavailable'
        AVAILABLE = 'available', 'Available'
        ADOPTED = 'adopted', 'Adopted'

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    breed = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.UNAVAILABLE
    )
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female')
    ])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class PetImage(models.Model):
    pet = models.ForeignKey(Pet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pets/')

    def clean(self):
        if self.pk is None:
            if self.pet_id and self.pet.images.count() >= 4:
                raise ValidationError("You can only have 4 images.")

class AdoptionRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    reason = models.TextField(blank=True, null=True, max_length=200)
    canceled_by_user = models.BooleanField(default=True)