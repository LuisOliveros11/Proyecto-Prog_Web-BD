# Generated by Django 4.2.6 on 2023-12-01 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PortalWeb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='comentario',
            field=models.TextField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='reporte',
            name='evidencia_fotografica',
            field=models.ImageField(blank=True, upload_to='media/'),
        ),
    ]
