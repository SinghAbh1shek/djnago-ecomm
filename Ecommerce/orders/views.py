from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItems
from products.models import VendorProducts
from django.contrib import messages
from accounts.models import Customer

@login_required(login_url="/accounts/login/")
def add_to_cart(request):
    try:
        customer = Customer.objects.get(user_ptr=request.user.id)

        product = request.GET.get('product_id')

        cart, _ = Cart.objects.get_or_create(customer = customer, is_paid = False)
        cart_items, _ = CartItems.objects.get_or_create(cart=cart, product=VendorProducts.objects.get(id = product))
        print(cart_items)
        cart_items.quantity += 1
        cart_items.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error(request, "Invalid Product  ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    



@login_required(login_url="/accounts/login/")
def remove_to_cart(request):
    try:
        customer = Customer.objects.get(user_ptr=request.user.id)

        product = request.GET.get('product_id')
        
        cart, _ = Cart.objects.get_or_create(customer = customer, is_paid = False)
        cart_items= CartItems.objects.filter(cart=cart, product=VendorProducts.objects.get(id = product))
        if cart_items.exists():
            cart_items = cart_items[0]
            cart_items.quantity -= 1

            if cart_items.quantity <=0:
                cart_items.delete()
            else:
                cart_items.save()


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error(request, "Invalid Product  ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
