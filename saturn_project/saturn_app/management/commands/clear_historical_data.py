from django.core.management.base import BaseCommand
from forex_app.models import HistoricalData

class Command(BaseCommand):
    help = 'Limpia todos los datos de la tabla historical_data'

    def handle(self, *args, **options):
        try:
            count = HistoricalData.objects.all().count()
            HistoricalData.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Se han eliminado {count} registros de la tabla historical_data."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al limpiar la tabla historical_data: {str(e)}"))