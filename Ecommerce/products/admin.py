from django.contrib import admin

# Register your models here.
from products.models import *
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BrandName)
admin.site.register(Product)
admin.site.register(VariantOptions)
admin.site.register(ProductImages)
admin.site.register(VendorProducts)