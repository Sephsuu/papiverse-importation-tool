from rest_framework import generics
from api.models import Branch
from api.serializer import BranchSerializer

class BranchCreate(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

