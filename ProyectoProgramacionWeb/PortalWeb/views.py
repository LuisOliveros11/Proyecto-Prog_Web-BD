from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Reporte
from .models import Usuario
from .models import Servidor_Publico
from werkzeug.security import generate_password_hash, check_password_hash
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib import messages



# Create your views here.
    
def inicio_sesion(request):
    if request.method == 'POST':
        usuario = None
        servidor_publico = None
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(correo_electronico=email)
        except Usuario.DoesNotExist:
            try:
                servidor_publico = Servidor_Publico.objects.get(correo_electronico=email)
            except Servidor_Publico.DoesNotExist:
                messages.error(request, 'El correo electrónico no existe. Verifica tu correo electrónico.')
                return render(request, 'inicio_sesion.html')
        
        if usuario is not None:
            if usuario and check_password_hash(usuario.contrasena, password):
                request.session['user_email'] = email  
                return redirect('home_user')
            else:
                messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')
                return render(request, 'inicio_sesion.html')
        else: 
            if servidor_publico is not None:
                if servidor_publico and check_password_hash(servidor_publico.contrasena, password):
                    request.session['user_email'] = email  
                    return redirect('home_admin')
                else:
                    messages.error(request, 'Contraseña incorrecta. Inténtalo de nuevo.')
                    return render(request, 'inicio_sesion.html')

    else:
        return render(request, 'inicio_sesion.html')


def registro(request):
        return render(request, 'registro.html', {'mensaje': "¡Registro exitoso!"})

def registrar_usuario(request):
    error = None
    mensaje_exito = None

    if request.method == 'POST':
        correo_electronico = request.POST.get('correo_email')
        nombre = request.POST.get('cliente_nombre')
        apellidos = request.POST.get('cliente_apellidos')
        num_telefono = request.POST.get('numero_telefono')
        contraseña = request.POST.get('password1')
        confirmar_contraseña = request.POST.get('password2')

        if not nombre.replace(" ", "").isalpha():
            error = 'El nombre solo puede contener letras o espacios en blanco. Inténtalo de nuevo.'
        elif not apellidos.replace(" ", "").isalpha():
            error = 'Los apellidos solo pueden contener letras o espacios en blanco. Inténtalo de nuevo.'
        elif not num_telefono.isdigit() or len(num_telefono) != 10:
            error = 'El número de teléfono debe contener exactamente 10 dígitos numéricos. Inténtalo de nuevo.'
        elif len(contraseña) < 8:
            error = 'La contraseña debe tener al menos 8 caracteres. Inténtalo de nuevo.'
        elif Usuario.objects.filter(correo_electronico=correo_electronico).exists():
            error = 'Este correo electrónico ya está registrado. Por favor, utiliza otro.'
        elif contraseña == confirmar_contraseña:
            contraseña = generate_password_hash(contraseña)
            nuevo_usuario = Usuario(
                correo_electronico=correo_electronico,
                nombre=nombre,
                apellidos=apellidos,
                num_telefono=num_telefono,
                contrasena=contraseña
            )
            nuevo_usuario.save()
            mensaje_exito = 'Registro exitoso. Ahora puedes iniciar sesión.'
        else:
            error = 'Las contraseñas no coinciden. Inténtalo de nuevo.'

    return render(request, 'registro.html', {'error': error, 'mensaje_exito': mensaje_exito})



def home_usuario(request):
    email = request.session.get('user_email')
    return render(request, 'home_user.html', {'user_email': email})

def llenar_formulario_usuario(request):
    error = None
    imagen_url = None
    mensaje_exito = None

    if request.method == 'POST':
        categoria_HTML = request.POST.get('categoriaReporte')
        descripcion_HTML = request.POST.get('descripcionReporte')
        ubicacion_HTML = request.POST.get('ubicacionReporte')
        evidencia_fotografica = request.FILES.get('evidenciaFotografica', None)

        user_email = request.session.get('user_email', None)

        if categoria_HTML != "Categoria del reporte" and evidencia_fotografica and user_email:
            usuario = Usuario.objects.get(correo_electronico=user_email)

            nuevo_Reporte = Reporte(
                categoria=categoria_HTML,
                descripcion=descripcion_HTML,
                ubicacion=ubicacion_HTML,
                evidencia_fotografica=evidencia_fotografica,
                correo_electronico_usuario=usuario
            )
            nuevo_Reporte.save()
            mensaje_exito = 'Reporte registrado correctamente'
            
        else:
            error = 'Elija una categoría correcta, adjunte una evidencia fotográfica y asegúrese de estar autenticado.'

    return render(request, 'llenar_formulario_user.html', {'error': error, 'mensaje_exito': mensaje_exito})



    
    ##return render(request, 'llenar_formulario_user.html')
def lista_reportes(request):
    if request.user.is_superuser:
        lista_reportes = Reporte.objects.all().order_by('-fecha')
    else:
        user_email = request.session.get('user_email', None)
        
        if user_email:
            lista_reportes = Reporte.objects.filter(correo_electronico_usuario__correo_electronico=user_email).order_by('-fecha')
        else:
            lista_reportes = Reporte.objects.none()

    return render(request, 'lista_reportes.html', {'reportes': lista_reportes})
    

def home_administrador(request):
    email = request.session.get('user_email')
    return render(request, 'home_admin.html', {'user_email': email})

def lista_reportes_admin(request):
    if request.method == 'POST':
        categoria_seleccionada = request.POST.get('categoriaReporte', 'Todos')
        estatus_seleccionado = request.POST.get('estatusReporte', 'Cualquiera')

        if categoria_seleccionada == 'Todos':
            if estatus_seleccionado == 'Cualquiera':
                lista_reportes_admin = Reporte.objects.all().order_by('-fecha')
            else:
                lista_reportes_admin = Reporte.objects.filter(estatus=estatus_seleccionado).order_by('-fecha')
        else:
            if estatus_seleccionado == 'Cualquiera':
                lista_reportes_admin = Reporte.objects.filter(categoria=categoria_seleccionada).order_by('-fecha')
            else:
                lista_reportes_admin = Reporte.objects.filter(categoria=categoria_seleccionada, estatus=estatus_seleccionado).order_by('-fecha')

        return render(request, 'lista_reportes_admin.html', {'reportes': lista_reportes_admin, 'categoria_seleccionada': categoria_seleccionada, 'estatus_seleccionado': estatus_seleccionado})

    lista_reportes_admin = Reporte.objects.all().order_by('-fecha')
    return render(request, 'lista_reportes_admin.html', {'reportes': lista_reportes_admin, 'categoria_seleccionada': 'Todos', 'estatus_seleccionado': 'Cualquiera'})

def edicion_reporte(request, id_recibido):
    reporte = Reporte.objects.get(id=id_recibido)
    return render(request, 'edicion_reporte.html', {'reporte': reporte})

def editar_reporte(request, id_recibido):
    reporte = Reporte.objects.get(id=id_recibido)

    estado = request.POST.get("estadoReporte")
    comentario = request.POST.get("comentarioDeReporte")

    reporte.estatus = estado
    reporte.comentario = comentario
    reporte.save()

    return redirect(lista_reportes_admin)

def edicion_reporte(request, id_recibido):
    reporte = Reporte.objects.get(id = id_recibido)
    return render(request, 'edicion_reporte.html', {'reporte': reporte})

def editar_reporte(request, id_recibido):
    reporte = Reporte.objects.get(id = id_recibido)

    estado = request.POST.get("estadoReporte")
    comentario = request.POST.get("comentarioDeReporte")

    reporte.estatus = estado
    reporte.comentario = comentario
    reporte.save()

    return redirect(lista_reportes_admin)

def ver_reporte_admin(request, id_recibido):
    if request.method == 'POST':
        return redirect(lista_reportes_admin)
    else:
        reporte = Reporte.objects.get(id = id_recibido)
        return render(request, "ver_reporte_admin.html", {'reporte': reporte})


    

    