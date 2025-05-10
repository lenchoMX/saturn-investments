from django.core.management.base import BaseCommand
from django.conf import settings
import psycopg2
from psycopg2 import Error

class Command(BaseCommand):
    help = 'Crea la base de datos saturn_db si no existe'

    def handle(self, *args, **options):
        db_config = settings.DATABASES['default']
        conn = None
        try:
            # Conectar a PostgreSQL (sin especificar base de datos para crear una nueva)
            conn = psycopg2.connect(
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT'],
                database='postgres'  # Conectar a la base de datos por defecto para crear una nueva
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Verificar si la base de datos ya existe
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_config['NAME'],))
            exists = cursor.fetchone()
            
            if not exists:
                # Crear la base de datos si no existe
                cursor.execute(f"CREATE DATABASE {db_config['NAME']}")
                self.stdout.write(self.style.SUCCESS(f"Base de datos '{db_config['NAME']}' creada con éxito."))
            else:
                self.stdout.write(self.style.WARNING(f"La base de datos '{db_config['NAME']}' ya existe."))
                
            cursor.close()
        except Error as e:
            self.stdout.write(self.style.ERROR(f"Error al crear la base de datos: {e}"))
        finally:
            if conn is not None:
                conn.close()
                self.stdout.write(self.style.SUCCESS("Conexión a PostgreSQL cerrada."))