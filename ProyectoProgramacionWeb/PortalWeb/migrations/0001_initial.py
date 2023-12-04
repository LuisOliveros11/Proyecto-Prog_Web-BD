# 0001_initial.py

from django.db import migrations, models
import django.db.models.deletion
from PortalWeb.models import create_servidores_publicos  # Asegúrate de importar la función correctamente

class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servidor_Publico',
            fields=[
                ('correo_electronico', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('nombre', models.TextField(max_length=200)),
                ('apellidos', models.TextField(max_length=200)),
                ('num_telefono', models.TextField()),
                ('puesto', models.TextField(max_length=200)),
                ('contrasena', models.CharField(max_length=250, default="ContrasenaDefault"))
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('correo_electronico', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('nombre', models.TextField(max_length=200)),
                ('apellidos', models.TextField(max_length=200)),
                ('num_telefono', models.TextField()),
                ('contrasena', models.CharField(default='ContrasenaDefault', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.TextField()),
                ('estatus', models.TextField(blank=True, default='Enviado', null=True)),
                ('descripcion', models.TextField()),
                ('ubicacion', models.TextField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('correo_electronico_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PortalWeb.usuario')),
            ],
        ),
        migrations.RunPython(create_servidores_publicos),
    ]