from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection, transaction
from django.apps import apps
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Borra las tablas de la aplicación core_app, vuelve a aplicar las migraciones específicas de core_app y ejecuta la importación de datos desde un archivo SQL.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Este comando borrará las tablas de la aplicación core_app de la base de datos, volverá a aplicar las migraciones específicas de core_app y ejecutará la importación de datos desde un archivo SQL.'))
        confirm = input('¿Estás seguro de que deseas continuar? (y/n): ')
        if confirm.lower() != 'y':
            self.stdout.write(self.style.ERROR('Operación cancelada.'))
            return

        try:
            # Lista de aplicaciones personalizadas cuyas tablas se eliminarán
            custom_apps = ['core_app', 'economic_events_app']
            
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
                    self.stdout.write(self.style.SUCCESS('Tablas de core_app borradas con éxito.'))
                else:
                    self.stdout.write(self.style.WARNING('No se encontraron tablas de core_app para borrar.'))
                
                # Eliminar entradas de migraciones aplicadas para core_app y economic_events_app de django_migrations
                self.stdout.write('Eliminando historial de migraciones aplicadas para core_app y economic_events_app...')
                cursor.execute("DELETE FROM django_migrations WHERE app IN ('core_app', 'economic_events_app');")
                self.stdout.write(self.style.SUCCESS('Historial de migraciones para core_app y economic_events_app eliminado.'))
            
            # Eliminar archivos de migración existentes para core_app y economic_events_app
            core_migration_dir = Path(__file__).resolve().parent.parent.parent / 'migrations'
            economic_events_migration_dir = Path(__file__).resolve().parent.parent.parent.parent / 'economic_events_app' / 'migrations'
            
            for migration_dir in [core_migration_dir, economic_events_migration_dir]:
                if migration_dir.exists():
                    self.stdout.write(self.style.WARNING(f'Eliminando archivos de migración existentes en {migration_dir}...'))
                    for migration_file in migration_dir.glob('*.py'):
                        if migration_file.name != '__init__.py':
                            try:
                                migration_file.unlink()
                                self.stdout.write(f'  Eliminado {migration_file.name}... OK')
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'  Error al eliminar {migration_file.name}: {str(e)}'))
                    self.stdout.write(self.style.SUCCESS(f'Archivos de migración eliminados con éxito en {migration_dir}.'))
                else:
                    self.stdout.write(self.style.WARNING(f'No se encontró el directorio de migraciones en la ruta: {str(migration_dir)}'))
            

            # Generar nuevas migraciones
            self.stdout.write(self.style.WARNING('Generando nuevas migraciones...'))
            call_command('makemigrations', 'core_app', 'economic_events_app', interactive=False, verbosity=2, no_input=True)
            self.stdout.write(self.style.SUCCESS('Nuevas migraciones generadas con éxito para core_app y economic_events_app.'))

            # Volver a aplicar las migraciones
            self.stdout.write(self.style.WARNING('Aplicando migraciones...'))
            call_command('migrate', interactive=False, verbosity=2)
            self.stdout.write(self.style.SUCCESS('Migraciones aplicadas con éxito para todas las aplicaciones.'))
            
            # Ejecutar importación de datos desde archivo SQL
            sql_file_path = Path(__file__).resolve().parent.parent.parent.parent / 'config' / 'sql' / 'supported_entity.sql'
            
            # En la sección de importación de datos
            if os.path.exists(sql_file_path):
                self.stdout.write(self.style.WARNING('Ejecutando importación de datos desde supported_entity.sql...'))
                with open(sql_file_path, 'r', encoding='utf-8') as sql_file:  # Especificar codificación UTF-8
                    sql_content = sql_file.read()
                
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(sql_content)
                        cursor.execute("SELECT COUNT(*) FROM core_app_supportedentity;")
                        row_count = cursor.fetchone()[0]
                
                self.stdout.write(self.style.SUCCESS(f'Datos importados con éxito: {row_count} filas insertadas desde supported_entity.sql.'))
            else:
                self.stdout.write(self.style.ERROR(f'No se encontró el archivo SQL en {sql_file_path}.'))

            # Importar también supported_minute.sql
            sql_minute_file_path = Path(__file__).resolve().parent.parent.parent.parent / 'config' / 'sql' / 'supported_minute.sql'
            if os.path.exists(sql_minute_file_path):
                self.stdout.write(self.style.WARNING('Ejecutando importación de datos desde supported_minute.sql...'))
                with open(sql_minute_file_path, 'r', encoding='utf-8') as sql_file:  # Especificar codificación UTF-8
                    sql_content = sql_file.read()
                
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        try:
                            cursor.execute(sql_content)
                            cursor.execute("SELECT COUNT(*) FROM core_app_supportedminute;")
                            total_count = cursor.fetchone()[0]
                            self.stdout.write(self.style.SUCCESS(f'Datos importados con éxito: {total_count} filas insertadas desde supported_minute.sql.'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error al ejecutar el archivo SQL: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'No se encontró el archivo SQL en {sql_minute_file_path}.'))

            # Importar datos de economic_events desde economic_events.sql
            economic_events_file_path = Path(__file__).resolve().parent.parent.parent.parent / 'config' / 'sql' / 'economic_events.sql'
            if os.path.exists(economic_events_file_path):
                self.stdout.write(self.style.WARNING('Ejecutando importación de datos desde economic_events.sql...'))
                with open(economic_events_file_path, 'r', encoding='utf-8') as sql_file:
                    sql_content = sql_file.read()
                    # Reemplazar el formato de fecha con zona horaria a un formato sin zona horaria
                    sql_content = sql_content.replace("+00:00", "")
                    # También manejar otros posibles formatos de zona horaria
                    sql_content = sql_content.replace("+00", "")
                    sql_content = sql_content.replace("-00:00", "")
                    sql_content = sql_content.replace("-00", "")
                    # Envolver las fechas en comillas simples si no lo están
                    import re
                    sql_content = re.sub(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', r"'\1'", sql_content)
                
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        try:
                            cursor.execute(sql_content)
                            cursor.execute("SELECT COUNT(*) FROM economic_events_app_economicevent;")
                            total_count = cursor.fetchone()[0]
                            self.stdout.write(self.style.SUCCESS(f'Datos importados con éxito: {total_count} filas insertadas desde economic_events.sql.'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error al ejecutar el archivo SQL: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'No se encontró el archivo de datos en {economic_events_file_path}.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la operación: {str(e)}'))
            raise  # Relanzar la excepción para depuración