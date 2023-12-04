"""
URL configuration for ProyectoProgramacionWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from PortalWeb import views
from django.contrib.auth import urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path ('', views.inicio_sesion, name='inicio_sesion'),
    path('admin/', admin.site.urls),
    path('registro/', views.registro),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('home_user/', views.home_usuario, name='home_user'),
    path('llenar_formulario_user/', views.llenar_formulario_usuario, name='llenar_formulario_user'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('home_admin/', views.home_administrador, name='home_admin'),
    path('reportes_admin/', views.lista_reportes_admin, name='lista_reportes_admin'),
    path('reportes_admin/edicion_reporte/<id_recibido>', views.edicion_reporte, name='edicion_reporte'),
    path('reportes_admin/edicion_reporte/editar_reporte/<id_recibido>', views.editar_reporte, name='editar_reporte'),
    path('reportes_admin/ver_reporte_admin/<id_recibido>', views.ver_reporte_admin, name="ver_reportes_admin")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
