from django.contrib import admin
from .models import Producto, Usuario

admin.site.register(Producto)
# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'rut', 'edad', 'correo', 'telefono')
    search_fields = ('nombres', 'rut', 'correo')