from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        else:
            return '/static/img/no-disponible.jpg'  # Ruta a la imagen predeterminada dentro de la aplicación

class Perfil(models.Model):
    ROLES = [
        ('cliente', 'Cliente'),
        ('superadmin', 'Superadmin'),
        ('preparador_fisico', 'Preparador Físico'),
        ('nutricionista', 'Nutricionista'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Relaciona el carrito con un usuario (opcional)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)



# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=50)  # Puede ser PayPal u otro método de pago
#     is_paid = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment for {self.cart} by {self.user.username}"


from django.db import models
from django.contrib.auth.models import User

class Usuario2(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    direccion = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombres} ({self.rut})'

    class Meta:
        ordering = ['nombres']








class Usuario(models.Model):
    rut = models.CharField(max_length=12, unique=True)  # Campo de texto para RUT, aseguramos que sea único
    nombres = models.CharField(max_length=100)  # Campo de texto para nombres
    edad = models.PositiveIntegerField()  # Campo numérico para la edad
    direccion = models.CharField(max_length=200)  # Campo de texto para la dirección
    correo = models.EmailField(unique=True)  # Campo de email, aseguramos que sea único
    telefono = models.CharField(max_length=15)  # Campo de texto para teléfono
    fecha_contrato = models.DateField()  # Campo de fecha para la fecha de contrato
    fecha_termino = models.DateField()  # Campo de fecha para la fecha de término de contrato

    def __str__(self):
        return f'{self.nombres} ({self.rut})'

    class Meta:
        ordering = ['nombres']  # Ordenar por nombres

