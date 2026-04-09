from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Order, Reservation, Review
from .serializers import BookSerializer, OrderSerializer, ReservationSerializer, ReviewSerializer
from .permissions import IsOperatorOrAdmin # We will define this below

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOperatorOrAdmin()]

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.filter(is_active=True)
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def clear_expired(self, request):
        # Manual trigger to clear reservations older than 24 hours
        expired_time = timezone.now() - timedelta(days=1)
        updated = Reservation.objects.filter(reserved_at__lt=expired_time, is_active=True).update(is_active=False)
        return Response({"message": f"Cleared {updated} expired reservations."})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOperatorOrAdmin]

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        order = self.get_object()
        order.actual_return_date = timezone.now()
        order.calculate_fine()
        return Response({"fine": order.fine_amount})

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)