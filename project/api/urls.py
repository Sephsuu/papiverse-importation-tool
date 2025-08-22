from django.urls import path
from api.views import BranchCreate

urlpatterns = [
    path('branches/', BranchCreate.as_view(), name='book-list-create'),  # Use .as_view() if it's a class-based view
]
