from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItems
from products.models import VendorProducts
from django.contrib import messages
from accounts.models import Customer
from .payments import RazorPayPayment
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="/accounts/login/")
def get_cart(request):
    cart = None
    payment_info = {}
    try:
        cart = Cart.objects.get(customer = request.user.customer, is_paid = False)
        amount = cart.getCartTotal()
        receipt = cart.customer.username
        payment = RazorPayPayment('INR')
        payment_info = payment.processPayment(amount*100, receipt)
        cart.order_id = payment_info['id']
        cart.save()

    except Exception as e:
        print(e)
    return render(request, 'cart.html', context={'cart': cart, 'payment_info': payment_info})

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
        quantity = request.GET.get('quantity')
        
        cart, _ = Cart.objects.get_or_create(customer = customer, is_paid = False)
        cart_items= CartItems.objects.filter(cart=cart, product=VendorProducts.objects.get(id = product))
        if cart_items.exists():
            cart_items = cart_items[0]
            if quantity:
                cart_items.quantity = int(quantity)
            else:
                cart_items.quantity -= 1

            if cart_items.quantity <=0:
                cart_items.delete()
            else:
                cart_items.save()


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error(request, "Invalid Product  ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required(login_url="/accounts/login/")
@csrf_exempt
def payment_success(request):
    try:
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        cart = Cart.objects.get(order_id = razorpay_order_id)
        cart.payment_id = razorpay_payment_id
        cart.signature = razorpay_signature
        cart.is_paid = True
        cart.convertToOrder()
        cart.save()

        return render(request, 'success.html')
    except Exception as e:
        print(e)
        return redirect('/')