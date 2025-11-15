from home.views import *
from django.urls import path, include

urlpatterns = [
    path('', home, name='home'),
    path('product-details/<product_id>/', product_details, name='product_details'),
    # path('registration/', include('accounts.urls')),
]
