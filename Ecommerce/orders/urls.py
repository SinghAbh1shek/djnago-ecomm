from .views import *
from django.urls import path

urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('remove-to-cart/', remove_to_cart, name='remove-to-cart'),
    path('cart/', get_cart, name='get_cart'),

]