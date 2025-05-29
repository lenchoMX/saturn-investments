from django.db import models

class SupportedEntity(models.Model):
    ENTITY_TYPES = (
        ('currency_pair', 'Par de divisas'),
        ('commodity', 'Commodity'),
        ('equity', 'Acción'),
        ('interest_rate', 'Tasa de interés'),
        ('cryptocurrency', 'Criptomoneda'),
    )

    name = models.CharField(max_length=10, unique=True, help_text="Ejemplo: EUR/USD, XAU/USD, AAPL")
    symbol = models.CharField(max_length=10, unique=True, help_text="Formato para historical_data, ej: EURUSD, XAUUSD, AAPL")
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES, help_text="Tipo de entidad")
    description = models.CharField(max_length=100, blank=True, help_text="Descripción opcional")
    active = models.BooleanField(default=True, help_text="Indica si la entidad está activa")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Entidad Soportada"
        verbose_name_plural = "Entidades Soportadas"

class SupportedMinute(models.Model):
    IMPACT_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    name = models.CharField(max_length=100, unique=True)  # Ej. "FOMC Minutes"
    description = models.TextField()  # Ej. "Discusión sobre tasas de interés en EE. UU."
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES, default='High')  # Impacto esperado
    country = models.CharField(max_length=50)  # Ej. "United States"
    source = models.CharField(max_length=100)  # Ej. "Federal Reserve"
    frequency = models.CharField(max_length=50)  # Ej. "Every 6 weeks"
    markets_affected = models.CharField(max_length=200)  # Ej. "Forex, Equities"
    symbols_affected = models.CharField(max_length=200)  # Ej. "EUR/USD, USD/JPY"

    def __str__(self):
        return f"{self.name} ({self.country})"
