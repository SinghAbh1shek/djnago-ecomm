from django.db import models
from utils.models import BaseModel
from accounts.models import Shopkeeper


class Category(BaseModel):
    name = models.CharField( max_length=100)
    comission_percentage = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField( max_length=100)
    def __str__(self):
        return self.name
    
class BrandName(BaseModel):
    name = models.CharField( max_length=100)
    def __str__(self):
        return self.name

class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product_sub_category')
    brand = models.ForeignKey(BrandName, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    product_descriptions = models.TextField()
    product_sku = models.CharField(max_length=100, unique=True)
    hsn_code = models.CharField(max_length=100)
    maximum_retail_price = models.FloatField()
    parent_product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='variant_product', null=True, blank=True)

    def __str__(self):
        return self.item_name

    def getFirstImage(self):
        if self.product_images.first():
            return self.product_images.first().image
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGZjYKPjVrCS_uKmuUXIkYNXPA3x0q_Y-hYQ&s'

class VariantOptions(BaseModel):
    variant_name = models.CharField(max_length=100)
    option_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.option_name

class ProductVariant(BaseModel):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    variant_option = models.ManyToManyField(VariantOptions)

    def __str__(self):
        return self.variant_option

class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

class VendorProducts(BaseModel):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    vendor_selling_price = models.FloatField()
    dealer_price = models.FloatField()
    is_active = models.BooleanField(default=True)
    delivery_fee = models.FloatField(default=0)

    def get_product_details(self):
        return {
            'product_name': self.product.item_name,
            'image': self.product.getFirstImage()
            }
            