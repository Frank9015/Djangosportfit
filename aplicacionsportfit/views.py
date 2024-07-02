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
import requests
import logging
import random
import decimal

from .models import Producto, Usuario, Usuario2, Perfil, Cart, CartItem, Contacto, Venta, FichaPaciente, Evolucion, Reserva
from .serializers import ProductoSerializer, ContactoSerializer, VentaSerializer, FichaPacienteSerializer, EvolucionSerializer, ReservaSerializer
from .forms import ContactoForm, FichaPacienteForm, EvolucionForm, ReservaHoraFormCliente, ReservaHoraFormPersonal, UsuarioForm

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
def checkout(request):
    if request.user.is_authenticated:
        carrito, _ = Cart.objects.get_or_create(user=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        carrito = get_object_or_404(Cart, id=carrito_id)

    total_clp = carrito.items.aggregate(total=Sum('producto__precio'))['total'] or 0
    tipo_cambio_clp_usd = 0.0012
    total_usd = total_clp * tipo_cambio_clp_usd

    context = {
        'carrito': carrito,
        'total_clp': total_clp,
        'total_usd': total_usd,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID
    }

    return render(request, 'checkout.html', context)

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
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = nombre
                user.last_name = f"{apellido_paterno} {apellido_materno}"
                user.save()
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            
    return render(request, 'registro.html')

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
        fichas = FichaPaciente.objects.filter(usuario=request.user)
        return render(request, 'dashboard_nutricionista.html', {'fichas': fichas})
    else:
        return redirect('index')

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
            form.save()
            return JsonResponse({'message': 'Ficha registrada exitosamente!'}, status=200)
        else:
            return JsonResponse({'message': 'Error al registrar la ficha.'}, status=400)
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
        cart_item.cantidad = nueva_cantidad
        cart_item.save()

    total = cart_item.cart.items.aggregate(Sum('producto__precio'))['producto__precio__sum']
    if total is None:
        total = 0

    return JsonResponse({'success': True, 'total': float(total)})
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


# Vista para reservas
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
            return JsonResponse({'message': 'Reserva realizada exitosamente!'}, status=200)
        else:
            return JsonResponse({'message': 'Error al realizar la reserva.'}, status=400)
    else:
        if request.user.perfil.rol in ['nutricionista', 'preparador_fisico']:
            form = ReservaHoraFormPersonal()
        else:
            form = ReservaHoraFormCliente()
    return render(request, 'reservar_hora.html', {'form': form})
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

def pay_with_paypal(request):
    # Obtener el carrito de compras y el usuario actual
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if cart:
        # Obtener todos los ítems en el carrito
        items_in_cart = CartItem.objects.filter(cart=cart)

        # Crear un objeto de pago de PayPal
        paypal_payment = {
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_success')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancel'))
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": item.producto.nombre,
                        "sku": "item",
                        "price": str(item.producto.precio),
                        "currency": "USD",
                        "quantity": item.cantidad
                    } for item in items_in_cart]
                },
                "amount": {
                    "total": str(sum(decimal.Decimal(item.producto.precio) * item.cantidad for item in items_in_cart)),
                    "currency": "USD"
                },
                "description": "Compra en nuestra tienda."
            }]
        }

        # Crear el pago en PayPal
        paypal_payment_object = Payment(paypal_payment)
        if paypal_payment_object.create():
            for link in paypal_payment_object.links:
                if link.method == "REDIRECT":
                    # Redirigir al usuario a PayPal para completar la transacción
                    return redirect(link.href)
        else:
            # Si hay un error, mostrar un mensaje de error al usuario
            return render(request, "payment_error.html", {"error": paypal_payment_object.error})

    return render(request, "payment_error.html", {"error": "Algo salió mal."})


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
        if request.user.groups.filter(name='Personal').exists():
            form = ReservaHoraFormPersonal(request.POST, user=request.user)
        else:
            form = ReservaHoraFormCliente(request.POST)
        
        if form.is_valid():
            reserva = form.save(commit=False)
            if not request.user.groups.filter(name='Personal').exists():
                reserva.usuario = request.user
            reserva.save()
            messages.success(request, 'La reserva se ha realizado correctamente.')
            return redirect('reserva_exitosa')  # Redirigir a una página de confirmación o éxito
        else:
            messages.error(request, 'Hubo un error en la reserva. Por favor, verifica los datos ingresados.')
    else:
        if request.user.groups.filter(name='Personal').exists():
            form = ReservaHoraFormPersonal(user=request.user)
        else:
            form = ReservaHoraFormCliente()

    context = {
        'form': form,
    }
    return render(request, 'reservar_hora.html', context)

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