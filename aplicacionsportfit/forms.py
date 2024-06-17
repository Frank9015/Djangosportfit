from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombres', 'edad', 'direccion', 'correo', 'telefono', 'fecha_contrato', 'fecha_termino']
