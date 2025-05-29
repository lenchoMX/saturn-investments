from django.db import models
from core_app.models import SupportedMinute

class EconomicEvent(models.Model):
    IMPACT_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    event_date = models.DateTimeField()
    country = models.CharField(max_length=50)
    event_name = models.CharField(max_length=255)
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES)
    actual = models.CharField(max_length=50, blank=True, null=True)
    forecast = models.CharField(max_length=50, blank=True, null=True)
    previous = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=100, default='MetaTrader 5')
    supported_minute = models.ForeignKey(SupportedMinute, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.event_name} ({self.country}) - {self.event_date}"