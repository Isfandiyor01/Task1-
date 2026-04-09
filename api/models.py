from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('operator', 'Operator'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Add these two lines to prevent the clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', # Unique name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', # Unique name
        blank=True
    )
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    available_copies = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    raken_at = models.DateTimeField(auto_now_add=True)
    return_deadline = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_fine(self):
        if self.actual_return_date and self.actual_return_date > self.return_deadline:
            overdue_days = (self.actual_return_date - self.return_deadline).days
            # 1% kuniga kechikish uchun
            self.fine_amount = ( overdue_days * self.book.daily_price ) * 0.01
            self.find_amount = fine
            self.save()
        else:
            self.fine_amount = 0.00
        self.save()
