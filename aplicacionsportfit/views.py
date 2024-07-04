from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from django.forms.utils import ErrorList
from django.utils.html import strip_tags
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseServerError, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, DatosEnvio, Venta, Recibo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.db import transaction
from .models import DatosEnvio, Venta, Recibo, Cart
from .forms import DatosEnvioForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseServerError
from .forms import DatosEnvioForm  # Importa tu formulario DatosEnvioForm
from .models import Cart, Venta, Recibo, DatosEnvio  # Importa todos los modelos relevantes
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.html import strip_tags
from django.db.models import F

import requests
import json

from django.conf import settings
from django.db import transaction

import requests
import logging
import random
import decimal

from .models import *
from .serializers import *
from .forms import *

logger = logging.getLogger(__name__)

# Index view
def index(request):
    todos_productos = Producto.objects.all()
    productos_destacados = random.sample(list(todos_productos), min(len(todos_productos), 3))
    otros_productos = [producto for producto in todos_productos if producto not in productos_destacados]

    return render(request, 'index.html', {
        'productos_destacados': productos_destacados,
        'otros_productos': otros_productos,
    })

# Galeria view
def galeria(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

# Carro view
def carro(request):
    return render(request, 'carro.html')

# Checkout view
@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    datos_envio_form = DatosEnvioForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'datos_envio_form': datos_envio_form,
    })

# Quienes somos view
def quienes_somos(request):
    return render(request, 'quienes_somos.html')

# Info producto view
def info_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'info_producto.html', {'producto': producto})

# Sabor Latino view
def saborlatino(request):
    api_url = "https://www.saborlatinochile.cl/duoc/servicio_web_sportfit.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        productos = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        productos = []
        error_message = "No se pudo conectar a la API de productos."
        return render(request, 'app/saborlatino.html', {'productos': productos, 'error_message': error_message})
    
    return render(request, 'saborlatino.html', {'productos': productos})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')

# Register view
def registrousuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        nombre = request.POST['nombre']
        apellido_paterno = request.POST['apellidoPaterno']
        apellido_materno = request.POST['apellidoMaterno']
        rut = request.POST['rut']
        direccion = request.POST['direccion']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso.')
            else:
                # Crear el usuario
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = nombre
                user.last_name = f"{apellido_paterno} {apellido_materno}"
                user.save()
                
                # Crear el perfil asociado con el rol de cliente
                perfil = Perfil.objects.create(user=user, rol='cliente')
                perfil.save()
                
                # Iniciar sesión automáticamente
                login(request, user)
                
                return redirect('index')  # Ajusta 'index' a la URL de tu página de inicio
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            
    return render(request, 'registrousuario.html')

# Contacto view
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Contacto enviado exitosamente!'}, status=200)
        else:
            return JsonResponse({'message': 'Error al enviar el contacto.'}, status=400)
    else:
        form = ContactoForm()
    return render(request, 'contacto.html', {'form': form})

# Dashboard nutricionista view
@login_required
def dashboard_nutricionista(request):
    if request.user.perfil.rol == 'nutricionista' or request.user.is_superuser:
        fichas = FichaPaciente.objects.all()  # Filtrar todas las fichas
        return render(request, 'dashboard_nutricionista.html', {'fichas': fichas})
    else:
        return redirect('index')  # Ajusta 'index' a la URL de tu página de inicio

# Dashboard preparador fisico view
@login_required
def dashboard_preparador_fisico(request):
    if request.user.perfil.rol == 'preparador_fisico' or request.user.is_superuser:
        evoluciones = Evolucion.objects.filter(ficha__usuario=request.user)
        return render(request, 'dashboard_preparador_fisico.html', {'evoluciones': evoluciones})
    else:
        return redirect('index')

# Registrar ficha view
@login_required
def registrar_ficha(request):
    if request.method == 'POST':
        form = FichaPacienteForm(request.POST)
        if form.is_valid():
            ficha_paciente = form.save(commit=False)
            # Calcular IMC y guardarlo en la instancia de FichaPaciente
            ficha_paciente.imc = ficha_paciente.peso / (ficha_paciente.altura ** 2)
            ficha_paciente.save()
            return JsonResponse({'message': 'Ficha registrada exitosamente!', 'imc': ficha_paciente.imc}, status=200)
        else:
            return JsonResponse({'message': 'Error al registrar la ficha.', 'errors': form.errors}, status=400)
    else:
        form = FichaPacienteForm()
    return render(request, 'registrar_ficha.html', {'form': form})

# Registrar evolucion view
@login_required
def registrar_evolucion(request):
    if request.method == 'POST':
        form = EvolucionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Evolución registrada exitosamente!'}, status=200)
        else:
            return JsonResponse({'message': 'Error al registrar la evolución.'}, status=400)
    else:
        form = EvolucionForm()
    return render(request, 'registrar_evolucion.html', {'form': form})

# Carrito view
def carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Cart.objects.get_or_create(user=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Cart.objects.get(id=carrito_id)
        else:
            carrito = None

    return render(request, 'carro_productos.html', {'carrito': carrito})

# Actualizar cantidad carrito view
@require_POST
def actualizar_cantidad_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    nueva_cantidad = int(request.POST.get('cantidad', 1))

    if nueva_cantidad > 0:
        # Guardar la cantidad anterior para posibles errores
        previous_quantity = cart_item.cantidad

        cart_item.cantidad = nueva_cantidad
        cart_item.save()

        # Recalcular el total del carrito después de actualizar la cantidad
        total = cart_item.cart.items.aggregate(Sum('producto__precio'))['producto__precio__sum']
        if total is None:
            total = 0

        return JsonResponse({'success': True, 'total': float(total)})
    else:
        return JsonResponse({'success': False, 'error': 'La cantidad debe ser mayor que cero.', 'previous_quantity': cart_item.cantidad})

@require_POST
@csrf_exempt
def agregar_al_carrito(request, producto_id):
    try:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id

        producto = get_object_or_404(Producto, id=producto_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)
        if not created:
            cart_item.cantidad += 1
        cart_item.save()

        return JsonResponse({'success': True, 'message': 'Producto agregado al carrito!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def obtener_carrito(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart).select_related('producto')

    items = []
    for item in cart_items:
        items.append({
            'producto': {
                'nombre': item.producto.nombre,
                'precio': item.producto.precio,
                'descripcion': item.producto.descripcion,
                'imagen': item.producto.imagen.url,
            },
            'cantidad': item.cantidad,
        })

    return JsonResponse({'cart_items': items})
# Eliminar del carrito view
@require_POST
@csrf_exempt
def eliminar_del_carrito(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        return JsonResponse({'success': True, 'message': 'Producto eliminado del carrito!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})




import decimal
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from paypalrestsdk import Payment
from .models import Cart, CartItem, Producto


@csrf_exempt
def confirmar_pago_paypal(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('paymentID')
        payer_id = data.get('payerID')
        token = data.get('token')

        url = f"https://api.sandbox.paypal.com/v1/payments/payment/{payment_id}/execute/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PAYPAL_CLIENT_ID}"
        }
        payload = {
            "payer_id": payer_id
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return JsonResponse({'success': True, 'message': 'Pago confirmado'})
        else:
            return JsonResponse({'success': False, 'message': 'Error al confirmar el pago'})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})

# NUTRICIONISTA


from django.shortcuts import render, redirect
from .forms import UsuarioForm
def success_page(request):
    return render(request, 'success.html')  # Asumiendo que tienes una plantilla 'success.html'
def register_view(request):
    # Lógica para la vista de registro
    return render(request, 'registro.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirigir a una página de éxito
    else:
        form = UsuarioForm()
    return render(request, 'registro.html', {'form': form})
    
@login_required
def reservar_hora(request):
    if request.method == 'POST':
        if request.user.perfil.rol in ['nutricionista', 'preparador_fisico']:
            form = ReservaHoraFormPersonal(request.POST)
        else:
            form = ReservaHoraFormCliente(request.POST)
        
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            return JsonResponse({'status': 'success', 'message': 'Reserva realizada exitosamente!'}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'message': 'Error al realizar la reserva.', 'errors': errors}, status=400)
    else:
        if request.user.perfil.rol in ['nutricionista', 'preparador_fisico']:
            form = ReservaHoraFormPersonal()
        else:
            form = ReservaHoraFormCliente()
    return render(request, 'reservar_hora.html', {'form': form})

@login_required
def historial(request):
    ventas = Venta.objects.filter(usuario=request.user)
    reservas = Reserva.objects.filter(usuario=request.user)
    
    context = {
        'ventas': ventas,
        'reservas': reservas,
    }
    return render(request, 'historial.html', context)

@login_required
def ver_reservasn(request):
    # Verificar que el usuario tenga el rol de nutricionista
    if request.user.perfil.rol == 'nutricionista':
        # Filtrar las reservas por la especialidad de nutricionista
        reservas = Reserva.objects.filter(especialidad='Nutricionista')
        return render(request, 'reservas_nutricionista.html', {'reservas': reservas})
    elif request.user.is_superuser:
        # Si es superusuario, puede ver todas las reservas
        reservas = Reserva.objects.all()
        return render(request, 'reservas_nutricionista.html', {'reservas': reservas})
    else:
        # Redirigir a la página de inicio si el usuario no tiene permisos suficientes
        return redirect('index')  # Ajusta 'index' a la URL de tu página de inicio

@login_required
def procesar_compra(request):
    if request.method == 'POST':
        print(request.POST)  # Para depuración
        form = DatosEnvioForm(request.POST)
        if form.is_valid():
            try:
                datos_envio = form.save(commit=False)
                datos_envio.usuario = request.user
                datos_envio.save()

                cart = Cart.objects.get(user=request.user)
                ventas_creadas = []
                recibos_creados = []

                with transaction.atomic():
                    for item in cart.items.all():
                        venta = Venta.objects.create(
                            usuario=request.user,
                            producto=item.producto,
                            cantidad=item.cantidad,
                            total=item.producto.precio * item.cantidad
                        )
                        ventas_creadas.append(venta)

                        recibo = Recibo.objects.create(
                            venta=venta
                        )
                        recibos_creados.append(recibo)

                        item.producto.stock = F('stock') - item.cantidad
                        item.producto.save()

                    cart.items.all().delete()

                return redirect('confirmacion_compra', recibo_id=recibo.id)

            except Exception as e:
                mensaje_error = f'Error al procesar la compra: {str(e)}'
                datos_depuracion = {
                    'Formulario de Datos de Envío': form.cleaned_data,
                    'Carrito del Usuario': list(cart.items.all().values_list('producto__nombre', 'cantidad')),
                    'Ventas Creadas': [venta.__dict__ for venta in ventas_creadas],
                    'Recibos Creados': [recibo.__dict__ for recibo in recibos_creados],
                }
                context = {
                    'mensaje': mensaje_error,
                    'datos': datos_depuracion,
                }
                return render(request, 'errores.html', context)
        else:
            errores = form.errors.as_data()
            mensaje_error = ""
            for campo, errores_lista in errores.items():
                for error in errores_lista:
                    mensaje_error += f"{campo.capitalize()}: {strip_tags(error)}<br>"

            context = {
                'mensaje': f'Formulario de datos de envío inválido:<br>{mensaje_error}',
                'datos': {
                    'Formulario de Datos de Envío': form.cleaned_data,
                    'Errores de Validación': errores,
                }
            }
            return render(request, 'errores.html', context)

    return redirect('checkout')
    
@login_required
def confirmacion_compra(request, recibo_id):
    recibo = get_object_or_404(Recibo, id=recibo_id)
    return render(request, 'confirmacion_compra.html', {'recibo': recibo})

@login_required
def paypal_return(request):
    if request.GET.get('payment_status') == 'Completed':
        recibo_id = request.GET.get('invoice')
        recibo = get_object_or_404(Recibo, id=recibo_id)

        # Aquí podrías agregar más lógica para procesar la venta si es necesario
        try:
            with transaction.atomic():
                # Actualizar el estado de la venta relacionada si es necesario
                venta = recibo.venta
                if not venta.pagada:
                    venta.pagada = True
                    venta.save()

                    # Procesar cualquier otra lógica necesaria para completar la venta

        except Exception as e:
            # Manejar cualquier error que ocurra durante el procesamiento de la venta
            mensaje_error = f'Error al procesar la venta: {str(e)}'
            context = {
                'mensaje': mensaje_error,
            }
            return render(request, 'errores.html', context)

        return redirect('confirmacion_compra', recibo_id=recibo.id)
    else:
        # El estado del pago no es 'Completed', redirigir al checkout
        return redirect('checkout')

@login_required
def ver_clientes(request):
    # Lógica para mostrar los clientes del nutricionista
    # Puedes implementar esta vista según la funcionalidad de tu aplicación
    return render(request, 'clientes.html')

def ver_errores(request):
    mensaje = "Errores al procesar la compra."
    # Supongamos que tienes datos específicos de depuración aquí
    datos = {
        'ejemplo': 'Información adicional de depuración.',
        'otro_ejemplo': ['Item 1', 'Item 2', 'Item 3'],
    }

    context = {
        'mensaje': mensaje,
        'datos': datos,
    }

    return render(request, 'errores.html', context)
    
@login_required
def obtener_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(SeguimientoPedido, pedido_id=pedido_id, usuario=request.user)
    return JsonResponse({'estado': pedido.estado, 'fecha_actualizacion': pedido.fecha_actualizacion})

# Tu vista para actualizar el estado del pedido
@csrf_exempt
@login_required
def actualizar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        nuevo_estado = data.get('estado')
        if nuevo_estado in dict(SeguimientoPedido.ESTADO_CHOICES):
            pedido = get_object_or_404(SeguimientoPedido, pedido_id=pedido_id, usuario=request.user)
            pedido.estado = nuevo_estado
            pedido.save()
            return JsonResponse({'estado': pedido.estado, 'fecha_actualizacion': pedido.fecha_actualizacion})
        return JsonResponse({'error': 'Estado inválido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class FichaPacienteViewSet(viewsets.ModelViewSet):
    queryset = FichaPaciente.objects.all()
    serializer_class = FichaPacienteSerializer

class EvolucionViewSet(viewsets.ModelViewSet):
    queryset = Evolucion.objects.all()
    serializer_class = EvolucionSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

class DatosEnvioViewSet(viewsets.ModelViewSet):
    queryset = DatosEnvio.objects.all()
    serializer_class = DatosEnvioSerializer

class ContratoEmpleadoViewSet(viewsets.ModelViewSet):
    queryset = ContratoEmpleado.objects.all()
    serializer_class = ContratoEmpleadoSerializer

class SeguimientoPedidoViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoPedido.objects.all()
    serializer_class = SeguimientoPedidoSerializer