# Generated by Django 5.2 on 2025-05-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EconomicEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField()),
                ('country', models.CharField(max_length=50)),
                ('event_name', models.CharField(max_length=255)),
                ('impact', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20)),
                ('actual', models.CharField(blank=True, max_length=50, null=True)),
                ('forecast', models.CharField(blank=True, max_length=50, null=True)),
                ('previous', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(default='MetaTrader 5', max_length=100)),
            ],
        ),
    ]
