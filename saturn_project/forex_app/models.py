from django.db import models
from django.utils import timezone

class HistoricalData(models.Model):
    pk = models.CompositePrimaryKey("timestamp", "symbol")
    timestamp = models.DateTimeField()
    symbol = models.CharField(max_length=10)
    market = models.CharField(max_length=50, null=True, blank=True)
    open_price = models.FloatField(null=True, blank=True)
    high_price = models.FloatField(null=True, blank=True)
    low_price = models.FloatField(null=True, blank=True)
    close_price = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    data_source = models.CharField(max_length=50, null=True, blank=True)
    timeframe = models.CharField(max_length=10, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'historical_data'
        indexes = [models.Index(fields=['symbol', 'timestamp'], name='idx_symbol')]
        constraints = [
            models.UniqueConstraint(fields=['timestamp', 'symbol'], name='unique_timestamp_symbol')
        ]
        managed = False

    def __str__(self):
        return f"{self.symbol} at {self.timestamp}"

class TempHistoricalData(models.Model):
    pk = models.CompositePrimaryKey("timestamp", "symbol")
    timestamp = models.DateTimeField()
    symbol = models.CharField(max_length=10)
    market = models.CharField(max_length=50, null=True, blank=True)
    open_price = models.FloatField(null=True, blank=True)
    high_price = models.FloatField(null=True, blank=True)
    low_price = models.FloatField(null=True, blank=True)
    close_price = models.FloatField(null=True, blank=True)
    volume = models.BigIntegerField(null=True, blank=True)
    data_source = models.CharField(max_length=50, null=True, blank=True)
    timeframe = models.CharField(max_length=10, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'temp_historical_data'
        indexes = [models.Index(fields=['symbol', 'timestamp'], name='idx_symbol_temp')]
        constraints = [
            models.UniqueConstraint(fields=['timestamp', 'symbol'], name='unique_timestamp_symbol_temp')
        ]
        managed = False

    def __str__(self):
        return f"{self.symbol} at {self.timestamp}"