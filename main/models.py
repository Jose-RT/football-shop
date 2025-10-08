from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=50)
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=50, null=True, blank=True) # Null dan blank untuk sehingga produk bisa tanpa brand

    def __str__(self):
        return self.name
    
# class Book(models.Model):
#     id = models.UUIDField()
#     title = models.CharField(max_length=255)

# class Author(models.Model):
#     bio = models.CharField()
#     books = models.ManyToManyField(Book)
#     user = models.OneToOneField(User)