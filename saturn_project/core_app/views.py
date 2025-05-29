from django.shortcuts import render, HttpResponse
from django.db import connection
from django.contrib.auth.decorators import login_required
from .models import SupportedEntity, SupportedMinute

def supported_entities(request):
    entities = SupportedEntity.objects.all()
    return render(request, 'core_app/supported_entities.html', {'entities': entities})

def supported_minutes_index(request):
    minutes = SupportedMinute.objects.all()
    return render(request, 'core_app/supported_minutes.html', {'minutes': minutes})

def symbols_list(request):
    symbols = SupportedEntity.objects.values_list('symbol', flat=True).distinct()
    return render(request, 'core_app/symbols_list.html', {'symbols': symbols})

def minutes_by_symbol(request, symbol):
    minutes = SupportedMinute.objects.filter(symbols_affected__contains=symbol)
    return render(request, 'core_app/minutes_by_symbol.html', {'minutes': minutes, 'symbol': symbol})

def events_by_minute(request, minute_id):
    # Aquí se debería implementar la lógica para mostrar eventos relacionados con una minuta específica
    # Por ahora, solo pasamos el ID de la minuta a la plantilla
    return render(request, 'core_app/events_by_minute.html', {'minute_id': minute_id})

def export_data(request):
    if request.method == 'POST':
        selected_tables = request.POST.getlist('tables')
        if not selected_tables:
            return render(request, 'core_app/export_data.html', {'tables': get_table_names(), 'error': 'No se seleccionaron tablas para exportar.'})
        
        sql_output = ""
        for table in selected_tables:
            sql_output += export_table_to_sql(table) + "\n\n"
        
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="database_export.sql"'
        response.write(sql_output)
        return response
    
    return render(request, 'core_app/export_data.html', {'tables': get_table_names()})

def get_table_names():
    with connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [row[0] for row in cursor.fetchall()]
    return tables

def export_table_to_sql(table_name):
    with connection.cursor() as cursor:
        # Obtener los nombres de las columnas
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = [row[0] for row in cursor.fetchall()]
        columns_str = ', '.join(columns)
        
        # Obtener los datos de la tabla
        cursor.execute(f"SELECT {columns_str} FROM {table_name};")
        rows = cursor.fetchall()
        
        # Generar el SQL para la exportación
        sql = f"-- Exportación de la tabla {table_name}\n"
        sql += f"INSERT INTO {table_name} ({columns_str}) VALUES\n"
        for i, row in enumerate(rows):
            values = []
            for value in row:
                if value is None:
                    values.append('NULL')
                elif isinstance(value, str):
                    values.append("'" + value.replace("'", "''") + "'")
                else:
                    values.append(str(value))
            sql += f"({', '.join(values)})"
            if i < len(rows) - 1:
                sql += ","
            sql += "\n"
        sql += ";"
        return sql
