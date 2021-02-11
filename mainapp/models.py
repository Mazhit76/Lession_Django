from os import name
from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    descripthion = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта',
                            max_length=128, blank=True)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(
        verbose_name='краткое описание', max_length=60, blank=True)
    descripthion = models.TextField(
        verbose_name='описание продукта', blank=True)
    price = models.DecimalField(
        verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(
        verbose_name='количество на складе', default=0)
    time_create = models.DateField(
        verbose_name='время создания', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')