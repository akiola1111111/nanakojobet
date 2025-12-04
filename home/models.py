from django.db import models


class FreeTip(models.Model):
    title = models.CharField(max_length=200)
    league = models.CharField(max_length=100) # New field for the league/competition
    teams = models.CharField(max_length=200) # New field for the teams playing
    description = models.TextField() # This will be the actual tip/prediction
    results = models.CharField(max_length=50, blank=True, null=True) # New field for the final result
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teams} - {self.title}"

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'Free Tip'
        verbose_name_plural = 'Free Tips'

class VIP(models.Model):
    title = models.CharField(max_length=200)
    league = models.CharField(max_length=100) # New field for the league/competition
    teams = models.CharField(max_length=200) # New field for the teams playing
    description = models.TextField() # This will be the actual tip/prediction
    results = models.CharField(max_length=50, blank=True, null=True) # New field for the final result
    date_posted = models.DateTimeField(auto_now_add=True)

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
