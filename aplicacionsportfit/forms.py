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
        fields = ['usuario', 'peso', 'altura']

        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso en kg'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Altura en metros'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.all()  # Opcional: Filtra aquí los usuarios si es necesario

    def save(self, commit=True):
        ficha = super().save(commit=False)
        ficha.imc = ficha.peso / (ficha.altura ** 2)
        if commit:
            ficha.save()
        return ficha
        
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

class ReservaHoraFormCliente(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'modalidad', 'especialidad', 'motivo']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': timezone.now().strftime('%Y-%m-%d'),
                    'class': 'form-control',
                    'placeholder': 'Seleccione una fecha'
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'Seleccione una hora'
                }
            ),
            'modalidad': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'especialidad': forms.Select(
                attrs={
                    'class': 'form-control',
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
        fields = ['usuario', 'fecha', 'hora', 'modalidad', 'especialidad', 'motivo']
        widgets = {
            'usuario': forms.HiddenInput(),
            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': timezone.now().strftime('%Y-%m-%d'),
                    'class': 'form-control',
                    'placeholder': 'Seleccione una fecha'
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'Seleccione una hora'
                }
            ),
            'modalidad': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'especialidad': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'motivo': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Motivo de la reserva'
                }
            ),
        }