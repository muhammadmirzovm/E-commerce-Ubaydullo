from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = "BUYER", "Buyer"
        SELLER = "SELLER", "Seller"
        
    
    role = models.CharField(
        choices=Role.choices,
        default=Role.BUYER
    )
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone_number = models.CharField(max_length=13, help_text="+998998889911")
    address = models.CharField(max_length=255) 
    
    def __str__(self):
        return f'{self.username} -> {self.role}'