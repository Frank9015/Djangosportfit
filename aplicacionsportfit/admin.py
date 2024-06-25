from django.contrib import admin
from .models import Producto, Usuario, Usuario2, Perfil

admin.site.register(Producto)
admin.site.register(Usuario2)
admin.site.register(Perfil)
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'rut', 'edad', 'correo', 'telefono')
    search_fields = ('nombres', 'rut', 'correo')