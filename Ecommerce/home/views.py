from django.shortcuts import render
from django.http import HttpResponse
from products.models import Category, Product, SubCategory, VendorProducts, ProductVariant

# Create your views here.
def home(request):

    categories = Category.objects.all()
    # sub_catogaries = SubCategory.objects.all()
    products = VendorProducts.objects.filter(product__product_images__isnull = False, product__parent_product__isnull = True)[:30]

    context = {
        "categories" : categories,
        "products" : products,
        # 'sub_catogaries': sub_catogaries,
    }

    return render(request, 'home/home.html', context)


def product_details(request, product_id):
    vendor_product = VendorProducts.objects.get(id = product_id)

    if request.GET.get('product_sku'):
        vendor_product = VendorProducts.objects.get(
            product__product_sku = request.GET.get('product_sku')
        )

    product_variants = []

    # print(vendor_product.product.variant_product.all())


    if vendor_product.product.product_variants.exists():
        variant_options = vendor_product.product.product_variants.prefetch_related('variant_option')
        
        for variant in variant_options:

            product_variants.extend({
                "product_sku": vendor_product.product.product_sku,
                "option_name": option.option_name,
                "variant_name": option.variant_name
            } for option in variant.variant_option.all()
            )

    variant_products = []
    if vendor_product.product.parent_product:
        variant_products = [vendor_product.product.parent_product]
    else:
        variant_products = vendor_product.product.variant_products.all()

    for vp in variant_products:
        product_variant = ProductVariant.objects.filter(product = vp).first()

        product_variants.extend({
            "product_sku": vp.product_sku,
            "option_name": option.option_name,
            "variant_name": option.variant_name
        } for option in product_variant.variant_option.all()
        )

    # print(product_variants)

    result = {}

    sorted_variants = sorted(product_variants, key = lambda x:x['product_sku'])
    for variant in sorted_variants:
        product_sku = variant['product_sku']
        variants_string = f"{variant['variant_name']} : {variant['option_name']}"

        if product_sku in result:
            result[product_sku].add(variants_string)
        else:
            result[product_sku] = {variants_string}
    
    for product_sku in result:
        result[product_sku] = " ".join(result[product_sku])

    # print(result)

    context = {"product": vendor_product, "product_variants": result}
    return render(request, 'home/product_details.html', context)
