from rest_framework import serializers
from .models import Producto, Contacto, Venta, FichaPaciente, Evolucion, Reserva

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class FichaPacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaPaciente
        fields = '__all__'

class EvolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evolucion
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'