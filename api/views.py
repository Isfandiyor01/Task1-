from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Book, Order
from .serializers import BookSerializer, OrderSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        order = self.get_object()
        if order.actual_return_date:
            return Response({"error": "Book already returned"}, status=400)
        
        order.actual_return_date = timezone.now()
        order.calculate_fine() # This uses the logic we wrote in models.py
        order.save()
        
        return Response({
            "status": "Book returned",
            "fine": order.fine_amount
        })
