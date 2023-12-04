from django.db import models
from django.utils.translation import gettext_lazy as _
from werkzeug.security import generate_password_hash


class Usuario(models.Model):
    correo_electronico = models.EmailField(primary_key=True)
    nombre = models.TextField(max_length=200, null=False)
    apellidos = models.TextField(max_length=200, null=False)
    num_telefono = models.TextField(null=False)
    contrasena = models.CharField(max_length=250, null=False, default="ContrasenaDefault")
    

    def __str__(self):
        return self.nombre + " " + self.apellidos

class Servidor_Publico(models.Model):
    correo_electronico = models.EmailField(primary_key=True)
    nombre = models.TextField(max_length=200, null=False)
    apellidos = models.TextField(max_length=200, null=False)
    num_telefono = models.TextField(null=False)
    puesto = models.TextField(max_length=200, null=False)
    contrasena = models.CharField(max_length=250, null=False, default="ContrasenaDefault")

    def __str__(self):
        return self.puesto + " " + self.nombre + " " + self.apellidos

class Reporte(models.Model):
    categoria = models.TextField(null=False)
    estatus = models.TextField(null=True, blank=True, default="Enviado")
    descripcion = models.TextField(null=False)
    ubicacion = models.TextField(null=False)
    fecha = models.DateField(auto_now_add=True)
    comentario = models.TextField(max_length=250, null=False, default="")
    correo_electronico_usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    evidencia_fotografica = models.ImageField(upload_to='media/', blank=True, null=False)
    
    def __str__(self):
        return self.categoria + " " + self.ubicacion
    

def create_servidores_publicos(apps, schema_editor):
    Servidor_Publico = apps.get_model('PortalWeb', 'Servidor_Publico')
    
    servidores_publicos_data = [
        {
            'correo_electronico': 'oscar@gmail.com',
            'nombre': 'Oscar',
            'apellidos': 'Aguilar Cota',
            'num_telefono': '612148891',
            'puesto': 'Administrador',
            'contrasena': generate_password_hash('oscar123'),
        },
        {
            'correo_electronico': 'eduardo@gmail.com',
            'nombre': 'Eduardo',
            'apellidos': 'Mendez Merino',
            'num_telefono': '6123436456',
            'puesto': 'Administrador',
            'contrasena': generate_password_hash('eduardo123'),
        },
        {
            'correo_electronico': 'aviles@gmail.com',
            'nombre': 'Kevin',
            'apellidos': 'Aviles Parra',
            'num_telefono': '6121537589',
            'puesto': 'Administrador',
            'contrasena': generate_password_hash('kevin123'),
        },
    ]

    for servidor_data in servidores_publicos_data:
        Servidor_Publico.objects.create(**servidor_data)