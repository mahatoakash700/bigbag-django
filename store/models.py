from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.


class Size(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='photos/products')
    sizes = models.ManyToManyField(Size, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
