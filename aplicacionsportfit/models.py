from django.db import models
from django.contrib.auth.models import User

# Modelo para los productos en la tienda

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
            return '/static/img/no-disponible.jpg'

# Modelo para los mensajes de contacto recibidos
class Contacto(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_contacto = models.DateTimeField(auto_now_add=True)
    destinatario = models.CharField(max_length=50, choices=[('nutricionista', 'Nutricionista'), ('preparador_fisico', 'Preparador Físico')])

    def __str__(self):
        return f"{self.nombre} - {self.email}"


# Modelo para las ventas realizadas
class Venta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - {self.usuario.username}"

# Modelo para los recibos asociados a las ventas
class Recibo(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=50)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recibo {self.id} - Venta {self.venta.id}"

# Modelo para la ficha de un paciente
class FichaPaciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    peso = models.FloatField()
    altura = models.FloatField()
    imc = models.FloatField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ficha {self.id} - {self.usuario.username}"

    def save(self, *args, **kwargs):
        self.imc = self.peso / (self.altura ** 2)
        super(FichaPaciente, self).save(*args, **kwargs)

# Modelo para la evolución de un paciente
class Evolucion(models.Model):
    ficha = models.ForeignKey(FichaPaciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    peso = models.FloatField()
    altura = models.FloatField()
    imc = models.FloatField(blank=True, null=True)
    comentarios = models.TextField()

    def __str__(self):
        return f"Evolución {self.id} - Ficha {self.ficha.id}"

    def save(self, *args, **kwargs):
        self.imc = self.peso / (self.altura ** 2)
        super(Evolucion, self).save(*args, **kwargs)

# Modelo para el perfil de usuario con roles
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

# Modelos para el carrito de compras
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

# Modelo adicional de usuario con datos personales
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

# Modelo original de usuario con contrato específico
class Usuario(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    direccion = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_contrato = models.DateField()
    fecha_termino = models.DateField()

    def __str__(self):
        return f'{self.nombres} ({self.rut})'

    class Meta:
        ordering = ['nombres']


class Reserva(models.Model):
    MODALIDAD_CHOICES = [
        ('Virtual', 'Virtual'),
        ('Presencial', 'Presencial'),
        ('sin datos', 'Sin datos'),  # Añade una opción de valor predeterminado
    ]

    ESPECIALIDAD_CHOICES = [
        ('Preparador físico', 'Preparador físico'),
        ('Nutricionista', 'Nutricionista'),
        ('sin datos', 'Sin datos'),  # Añade una opción de valor predeterminado
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES, default='sin datos')
    especialidad = models.CharField(max_length=20, choices=ESPECIALIDAD_CHOICES, default='sin datos')
    motivo = models.TextField()

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.fecha} a las {self.hora}"

class DatosEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"Datos de Envío {self.id} - {self.usuario.username}"


class ContratoEmpleado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)  # Suponiendo formato estándar para RUT chileno
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    rol = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    codigo_postal = models.CharField(max_length=20, null=True, blank=True)
    # Otros campos según necesidades

    def __str__(self):
        return f"Contrato de {self.nombre} ({self.usuario.username})"