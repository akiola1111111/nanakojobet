from django.db import models
from django.utils import timezone
from datetime import date

class FreeTip(models.Model):
    title = models.CharField(max_length=200)
    league = models.CharField(max_length=100)
    teams = models.CharField(max_length=200)
    description = models.TextField()
    results = models.CharField(max_length=50, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    # Remove individual booking code
    # booking_code = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., 1X2-ABC-123")

    def __str__(self):
        return f"{self.teams} - {self.title}"

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'Free Tip'
        verbose_name_plural = 'Free Tips'

class VIP(models.Model):
    title = models.CharField(max_length=200)
    league = models.CharField(max_length=100)
    teams = models.CharField(max_length=200)
    description = models.TextField()
    results = models.CharField(max_length=50, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    # Remove individual booking code
    # booking_code = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., 1X2-ABC-123")

    def __str__(self):
        return f"{self.teams} - {self.title}"

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'VIP Tip'
        verbose_name_plural = 'VIP'

class AdminPayment(models.Model):
    email = models.EmailField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin Payment by {self.email} - Ref: {self.reference}"

# Add a new model for date-based booking codes
class DailyBookingCode(models.Model):
    date = models.DateField(unique=True)
    free_tips_code = models.CharField(max_length=20, blank=True, null=True, help_text="Booking code for free tips")
    vip_code = models.CharField(max_length=20, blank=True, null=True, help_text="Booking code for VIP tips")
    
    def __str__(self):
        return f"Booking codes for {self.date}"
