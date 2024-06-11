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
from .models import Producto
import random
# from .models import Product 
#from .cart import carro_productos
# Create your views here.

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

def checkout(request):
    return render (request, 'checkout.html')

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la página principal u otra página después de iniciar sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

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


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('carro_productos')  

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
