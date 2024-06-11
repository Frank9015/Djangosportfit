from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

# class ShoppingCart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

#     def total_price(self):
#         return self.quantity * self.product.price

# class Payment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=50)  # Puede ser PayPal u otro método de pago
#     is_paid = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment for {self.cart} by {self.user.username}"



