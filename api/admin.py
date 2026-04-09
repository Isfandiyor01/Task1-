from django.contrib import admin
from .models import User, Book, Order, Reservation, Review


admin.site.register(User)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Reservation)
admin.site.register(Review)

# Register your models here.
