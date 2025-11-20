from django.db import models
from accounts.models import Customer
from products.models import VendorProducts
from django.db.models import Sum, F
from utils.utility import generateOrderId, getImageBase64, generateOrderPdf


# Create your models here.

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_cart')
    is_paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    signature = models.CharField(max_length=1000, null=True, blank=True)

    def calculateDeliveryFee(self):
        total = self.cart_items.aggregate(
            total = Sum(F('product__delivery_fee'))
        )['total']
        return total or 0
    
    def getCartTotal(self):
        total = self.cart_items.aggregate(
            total = Sum(F('product__vendor_selling_price') * F('quantity'))
        )['total']
        return total or 0
    
    def convertToOrder(self):
        if not Order.objects.filter(cart = self).exists():
            order = Order.objects.create(        
                cart = self,
                customer = self.customer,
                payment_id = self.payment_id,
                signature = self.signature,
                total = self.getCartTotal(),
            )
            for cart_item in self.cart_items.all():
                OrderItems.objects.create(
                    order = order,
                    product = cart_item.product,
                    quantity = cart_item.quantity,
                    price = cart_item.product.vendor_selling_price * cart_item.quantity
                )
            generateOrderPdf(order, order.getOrderData())

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(VendorProducts, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)

    def getCartItemsTotal(self):
        return self.product.vendor_selling_price * self.quantity
    

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_order')
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    signature = models.CharField(max_length=1000, null=True, blank=True)
    total = models.FloatField()
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.order_id = generateOrderId(str(Order.objects.count()+1))
        super(Order, self).save(*args, **kwargs)

    def getOrderData(self):
        data = {
            "customer": {
                "name": self.customer.first_name,
                'phone_number': self.customer.username,
            },
            "order": {
                "order_id": self.order_id,
                'total': self.total,
            },
            "order_items": []
        }
        order_items = [
            {
                'product': item.product.product.item_name,
                'image': getImageBase64(item.product.product.getFirstImageForPdf()),
                'quantity': item.quantity,
                'price': item.price/item.quantity,
                'total_price': item.price
            }
            for item in self.order_items.all()
        ]
        data['order_items'] = order_items
        return data

    def __str__(self):
        return self.order_id

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(VendorProducts, on_delete=models.SET_NULL, null= True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
