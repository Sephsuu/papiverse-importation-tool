from rest_framework.views import APIView
from api.serializer import FileUploadSerializer
from api.tools import Retriever
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json
import pandas as pd

class ReadPaidOrders(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                df = pd.read_excel(excel_file, sheet_name='Paid order list')
                rt = Retriever()
                for index, row in df.iterrows():
                    rt.populate_paid_order_list(row)

                safe_data = rt.clean_data(rt.paid_order_items)
                return Response(safe_data)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReadPaidOrdersJson(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                df = pd.read_excel(excel_file, sheet_name='Paid order list')
                rt = Retriever()
                for index, row in df.iterrows():
                    rt.populate_paid_order_list(row)

                safe_data = rt.clean_data(rt.paid_order_items)

                # Serialize to JSON string
                json_data = json.dumps(safe_data, indent=4)

                # Return as downloadable file
                response = HttpResponse(
                    json_data,
                    content_type='application/json'
                )
                response['Content-Disposition'] = 'attachment; filename="paid_orders.json"'
                return response

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReadCategoryItems(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                df = pd.read_excel(excel_file, sheet_name='Product report', header=1)
                rt = Retriever()
                for index, row in df.iterrows():
                    rt.populate_categories(row)

                safe_data = rt.clean_data(rt.category_items)
                return Response(safe_data)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReadProductItems(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                df = pd.read_excel(excel_file, sheet_name='Product report', header=1)
                rt = Retriever()
                for index, row in df.iterrows():
                    rt.populate_products(row)

                safe_data = rt.clean_data(rt.product_items)
                return Response(safe_data)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)