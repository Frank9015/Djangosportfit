from django import forms
from .models import *
from django import forms
from .models import Reserva
from django.utils import timezone

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombres', 'edad', 'direccion', 'correo', 'telefono', 'fecha_contrato', 'fecha_termino']

class ContactoForm(forms.ModelForm):
    destinatario = forms.ChoiceField(choices=[
        ('soporte', 'Soporte'),
        ('ventas', 'Ventas'),
        ('preparador fisico', 'Preparador Fisico'),
        ('nutricionista', 'Nutricionista')
    ], widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje', 'destinatario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mensaje', 'rows': 4}),
            'destinatario': forms.Select(attrs={'class': 'form-select'})
        }

class FichaPacienteForm(forms.ModelForm):
    class Meta:
        model = FichaPaciente
        fields = '__all__'
        widgets = {
            'usuario': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Altura'}),
        }
class EvolucionForm(forms.ModelForm):
    class Meta:
        model = Evolucion
        fields = '__all__'
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Altura'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comentarios', 'rows': 4}),
        }


from django import forms
from .models import Reserva
from django.utils import timezone

class ReservaHoraFormCliente(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',  # Usa el tipo de entrada HTML5 para fechas
                    'min': timezone.now().strftime('%Y-%m-%d'),  # Fecha mínima es hoy
                    'class': 'form-control',
                    'placeholder': 'Seleccione una fecha'
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',  # Usa el tipo de entrada HTML5 para horas
                    'class': 'form-control',
                    'placeholder': 'Seleccione una hora'
                }
            ),
            'motivo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Motivo de la reserva'
                }
            ),
        }

class ReservaHoraFormPersonal(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['usuario', 'fecha', 'hora', 'motivo']
        widgets = {
            'usuario': forms.HiddenInput(),
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',  # Usa el tipo de entrada HTML5 para fechas
                    'min': timezone.now().strftime('%Y-%m-%d'),  # Fecha mínima es hoy
                    'class': 'form-control',
                    'placeholder': 'Seleccione una fecha'
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',  # Usa el tipo de entrada HTML5 para horas
                    'class': 'form-control',
                    'placeholder': 'Seleccione una hora'
                }
            ),
            'motivo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Motivo de la reserva'
                }
            ),
        }
