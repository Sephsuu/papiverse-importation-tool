from django.urls import path
from api.views import BranchCreate, ReadPaidOrders, ReadCategoryItems, ReadProductItems

urlpatterns = [
    path('branches', BranchCreate.as_view(), name='book-list-create'),  
    path('read-paid-orders', ReadPaidOrders.as_view(), name='read-paid-orders'),
    path('read-category-items', ReadCategoryItems.as_view(), name='read-category-items'),
    path('read-product-items', ReadProductItems.as_view(), name='read-product-items'),
]
