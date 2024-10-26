from datetime import datetime
from os.path import join
from time import strptime

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=50)
    creative = models.CharField(max_length=50, default='Unknown')
    cover_img = models.ImageField(verbose_name='Cover Image', blank=True)
    is_released = models.BooleanField(default=False, verbose_name='Released')
    released_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORIES = [
        ('Anklets', 'Anklets'),
        ('Bracelets', 'Bracelets'),
        ('Earrings', 'Earrings'),
        ('Hair', 'Hair Jewellery'),
        ('Necklace', 'Necklace'),
        ('Other', 'Other'),
        ('Phone', 'Phone Accessories'),
        ('Waistbeads', 'Waistbeads'),

    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORIES, default='Earrings')
    price = models.IntegerField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    src = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.src
