from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse
import requests
import logging
# from .models import  Cart, ShoppingCart
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Producto, Usuario
import random
# from .models import Product 
#from .cart import carro_productos
# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # Obtener todos los productos
    todos_productos = Producto.objects.all()

    # Seleccionar aleatoriamente algunos productos para mostrar como destacados
    productos_destacados = random.sample(list(todos_productos), min(len(todos_productos), 3))

    # Obtener otros productos que no están en la lista de productos destacados
    otros_productos = [producto for producto in todos_productos if producto not in productos_destacados]

    return render(request, 'index.html', {
        'productos_destacados': productos_destacados,
        'otros_productos': otros_productos,
    })

def contacto(request):
    return render(request, 'contacto.html')

def galeria(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def carro(request):
    return render(request, 'carro.html')

import yfinance as yf
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Cart

def checkout(request):
    if request.user.is_authenticated:
        carrito, _ = Cart.objects.get_or_create(user=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        carrito = get_object_or_404(Cart, id=carrito_id)

    total_clp = carrito.items.aggregate(total=Sum('producto__precio'))['total'] or 0

    # Convertir a dólares usando yfinance
    try:
        ticker = yf.Ticker("CLPUSD=X")
        data = ticker.history(period="1d")
        tasa_cambio = data['Close'][0]

        print(f"Tasa de cambio obtenida: {tasa_cambio}")  # Depuración: imprimir la tasa de cambio
        
        total_usd = round(float(total_clp) / tasa_cambio, 2)  # Convertir total_clp a float antes de dividir
    except Exception as e:
        total_usd = 0.0
        print(f"Error al obtener la tasa de cambio: {e}")

    # Pasar los totales al contexto
    context = {
        'carrito': carrito,
        'total_clp': total_clp,
        'total_usd': total_usd,
    }

    return render(request, 'checkout.html', context)





def quienes_somos(request):
    return render (request, 'quienes_somos.html' )

def info_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'info_producto.html', {'producto': producto})

logger = logging.getLogger(__name__)

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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('index')  # Redirige a la página principal u otra página después de iniciar sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirige al usuario a la página de inicio después de cerrar sesión  


def register_view(request):
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
                return redirect('index')  # Redirige a la página principal u otra página después del registro
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            
    return render(request, 'registro.html')




# views.py
from django.shortcuts import render
from django.core.mail import send_mail

def contacto_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        email = request.POST.get('email', '')
        tipo_solicitud = request.POST.get('tipo_solicitud', '')
        mensaje = request.POST.get('mensaje', '')
        recibir_avisos = request.POST.get('avisos', False)

        # Aquí puedes agregar la lógica para enviar el correo, por ejemplo:
        send_mail(
            f'Solicitud de {tipo_solicitud} de {nombre}',
            f'Correo de contacto: {email}\n\nMensaje: {mensaje}',
            'tu@email.com',
            ['destinatario@email.com'],
            fail_silently=False,
        )

        # Luego de enviar el correo, podrías redirigir a una página de éxito o mostrar un mensaje
        return render(request, 'app/contacto_exitoso.html')

    return render(request, 'contacto.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem, Producto

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

@require_POST
def actualizar_cantidad_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    nueva_cantidad = int(request.POST.get('cantidad', 1))

    if nueva_cantidad > 0:
        cart_item.cantidad = nueva_cantidad
        cart_item.save()

    total = cart_item.cart.items.aggregate(models.Sum('producto__precio'))['producto__precio__sum']
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

        return JsonResponse({'success': True})

    except Producto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'El producto no existe.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Ocurrió un error: {str(e)}'})



@require_POST
def eliminar_del_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    # Calcular el nuevo total del carrito después de eliminar el ítem
    nuevo_total = calcular_total_carrito(request.user)
    return JsonResponse({'success': True, 'total': nuevo_total})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Usuario2, Perfil  # Asegúrate de importar tus modelos

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
        edad = request.POST['edad']
        telefono = request.POST['telefono']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso.')
            elif Usuario2.objects.filter(rut=rut).exists():
                messages.error(request, 'El RUT ya está en uso.')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.first_name = nombre
                user.last_name = f"{apellido_paterno} {apellido_materno}"
                user.save()

                perfil = Perfil(user=user, rol='cliente')
                perfil.save()

                usuario2 = Usuario2(
                    rut=rut,
                    nombres=f"{nombre} {apellido_paterno} {apellido_materno}",
                    edad=edad,
                    direccion=direccion,
                    correo=email,
                    telefono=telefono,
                    user=user
                )
                usuario2.save()

                login(request, user)
                messages.success(request, 'Registro exitoso. Bienvenido!')
                return redirect('index')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            
    return render(request, 'registrousuario.html')

# from paypalrestsdk import Payment

# def pay_with_paypal(request):
#     # Obtener el carrito de compras y el usuario actual
#     user = request.user
#     shopping_cart = ShoppingCart.objects.filter(user=user)

#     # Crear un objeto de pago de PayPal
#     payment = Payment({
#         "intent": "sale",
#         "payer": {
#             "payment_method": "paypal"
#         },
#         "redirect_urls": {
#             "return_url": "http://localhost:8000/payment/success/",
#             "cancel_url": "http://localhost:8000/payment/cancel/"
#         },
#         "transactions": [{
#             "item_list": {
#                 "items": [{
#                     "name": item.product.name,
#                     "sku": "item",
#                     "price": str(item.product.price),
#                     "currency": "USD",
#                     "quantity": item.quantity
#                 } for item in shopping_cart]
#             },
#             "amount": {
#                 "total": str(sum(item.total_price() for item in shopping_cart)),
#                 "currency": "USD"
#             },
#             "description": "Compra en nuestra tienda."
#         }]
#     })

#     # Crear el pago en PayPal
#     if payment.create():
#         for link in payment.links:
#             if link.method == "REDIRECT":
#                 # Redirigir al usuario a PayPal para completar la transacción
#                 return HttpResponseRedirect(link.href)
#     else:
#         # Si hay un error, mostrar un mensaje de error al usuario
#         return render(request, "payment_error.html", {"error": payment.error})


# NUTRICIONISTA


from django.shortcuts import render, redirect
from .forms import UsuarioForm
def success_page(request):
    return render(request, 'success.html')  # Asumiendo que tienes una plantilla 'success.html'
def registro(request):
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


