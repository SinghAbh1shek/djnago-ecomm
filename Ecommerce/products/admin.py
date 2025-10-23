from django.contrib import admin

# Register your models here.
from products.models import *
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BrandName)

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "sub_category",
        "brand",
        "item_name",
        "product_descriptions",
        "product_sku",
        "hsn_code",
        "maximum_retail_price",
        "parent_product",
    ]
    search_fields = [
        "item_name",
        "product_descriptions",
        "hsn_code",
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(VariantOptions)
admin.site.register(ProductImages)
admin.site.register(VendorProducts)