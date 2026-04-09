from rest_framework import serializers
from .models import Book, Order, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    fine_amount = serializers.ReadOnlyField() # Calculated automatically
    
    class Meta:
        model = Order
        fields = '__all__'