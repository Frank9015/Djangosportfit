from django.contrib import admin
from .models import Producto, Usuario, Usuario2, Perfil, Venta, Recibo, Reserva, DatosEnvio, Contacto

admin.site.register(Producto)
admin.site.register(Usuario2)
admin.site.register(Perfil)
admin.site.register(Venta)
admin.site.register(Recibo)
admin.site.register(Reserva)
admin.site.register(DatosEnvio)
admin.site.register(Contacto) 
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'rut', 'edad', 'correo', 'telefono')
    search_fields = ('nombres', 'rut', 'correo')