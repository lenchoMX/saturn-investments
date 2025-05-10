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
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES, help_text="Tipo de entidad")
    description = models.CharField(max_length=100, blank=True, help_text="Descripción opcional")
    active = models.BooleanField(default=True, help_text="Indica si la entidad está activa")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Entidad Soportada"
        verbose_name_plural = "Entidades Soportadas"
