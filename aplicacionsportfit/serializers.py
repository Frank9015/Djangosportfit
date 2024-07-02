from rest_framework import serializers
from .models import Producto, Contacto, Venta, FichaPaciente, Evolucion, Reserva, Perfil

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

class PerfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)

    class Meta:
        model = Perfil
        fields = ['username', 'email', 'rol', 'is_superuser']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.user.is_superuser:
            representation['rol'] = 'superadmin'
        return representation