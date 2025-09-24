from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["user", "name", "price", "description", "thumbnail", "category", "is_featured", "stock", "brand"]