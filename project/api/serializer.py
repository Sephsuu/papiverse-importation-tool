from rest_framework import serializers
from api.models import Branch

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'