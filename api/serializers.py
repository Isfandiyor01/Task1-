from rest_framework import serializers
from .models import Book, Order, Reservation, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta: model = Book; fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta: model = Order; fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta: model = Reservation; fields = ['id', 'book', 'reserved_at', 'is_active']
    read_only_fields = ['user']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta: model = Review; fields = '__all__'