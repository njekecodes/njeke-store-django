from datetime import datetime
from os.path import join
from time import strptime

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
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
        ('anklet', 'anklet'),
        ('bracelet', 'bracelet'),
        ('earrings', 'earrings'),
        ('hair', 'hair jewellery'),
        ('necklace', 'necklace'),
        ('other', 'other'),
        ('phone', 'phone accessories'),
        ('waist', 'waist beads'),

    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORIES, default='Earrings')
    price = models.IntegerField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image


class Review(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField()
    comment = models.TextField(max_length=200)
    person = models.CharField(max_length=50, default='Unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title