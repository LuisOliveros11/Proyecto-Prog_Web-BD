from django.contrib import admin
from .models import Usuario, Servidor_Publico, Reporte

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Servidor_Publico)
admin.site.register(Reporte)