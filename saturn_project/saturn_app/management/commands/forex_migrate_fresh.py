from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.apps import apps

class Command(BaseCommand):
    help = 'Borra las tablas de la aplicación forex_app y vuelve a aplicar las migraciones específicas de forex_app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Este comando borrará las tablas de la aplicación forex_app de la base de datos y volverá a aplicar las migraciones específicas de forex_app.'))
        confirm = input('¿Estás seguro de que deseas continuar? (y/n): ')
        if confirm.lower() != 'y':
            self.stdout.write(self.style.ERROR('Operación cancelada.'))
            return

        try:
            # Lista de aplicaciones personalizadas cuyas tablas se eliminarán
            custom_apps = ['forex_app']
            
            # Obtener todas las tablas de la base de datos
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                all_tables = [row[0] for row in cursor.fetchall()]
                
                # Obtener modelos de las aplicaciones personalizadas para identificar sus tablas
                custom_tables = []
                for app_label in custom_apps:
                    app_config = apps.get_app_config(app_label)
                    for model in app_config.get_models():
                        table_name = model._meta.db_table
                        if table_name in all_tables:
                            custom_tables.append(table_name)
                
                if custom_tables:
                    self.stdout.write(self.style.WARNING('Drop migrations:'))
                    for table in custom_tables:
                        self.stdout.write(f'  Dropping table {table}... OK')
                        cursor.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')
                    self.stdout.write(self.style.SUCCESS('Tablas de forex_app borradas con éxito.'))
                else:
                    self.stdout.write(self.style.WARNING('No se encontraron tablas de forex_app para borrar.'))
                
                # Eliminar entradas de migraciones aplicadas para forex_app de django_migrations
                self.stdout.write('Eliminando historial de migraciones aplicadas para forex_app...')
                cursor.execute("DELETE FROM django_migrations WHERE app = 'forex_app';")
                self.stdout.write(self.style.SUCCESS('Historial de migraciones para forex_app eliminado.'))
            
            # Volver a aplicar las migraciones
            self.stdout.write(self.style.WARNING('Running migrations:'))
            call_command('migrate', 'forex_app', interactive=False, verbosity=2)
            self.stdout.write(self.style.SUCCESS('Migraciones aplicadas con éxito para forex_app.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la operación: {str(e)}'))