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
    
    def __str__(self):
        return f'{self.username} -> {self.role}'