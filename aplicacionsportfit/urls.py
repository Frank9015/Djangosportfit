from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from rest_framework import routers

# Define los viewsets para el router de Django REST Framework
router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'contactos', ContactoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'fichas', FichaPacienteViewSet)
router.register(r'evoluciones', EvolucionViewSet)
router.register(r'reservas', ReservaViewSet)

# Define las URLs
urlpatterns = [
    path('', index, name='index'),
    path('contacto/', contacto, name='contacto'),
    path('dashboard/nutricionista/', dashboard_nutricionista, name='dashboard_nutricionista'),
    path('dashboard/preparador_fisico/', dashboard_preparador_fisico, name='dashboard_preparador_fisico'),
    path('registrar/ficha/', registrar_ficha, name='registrar_ficha'),
    path('registrar/evolucion/', registrar_evolucion, name='registrar_evolucion'),
    path('api/', include(router.urls)),  # Incluye las URLs generadas por el router
    # URLs anteriores que se mantenían
    path('galeria/', galeria, name='galeria'),
    path('saborlatino/', saborlatino, name='saborlatino'),
    path('carro/', carro, name='carro'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('checkout/', checkout, name='checkout'),
    path('registrousuario/', registrousuario, name='registrousuario'),
    path('info/<int:producto_id>/', info_producto, name='infoproducto'),
    path('quienes/', quienes_somos, name='quienes'),
    path('registro_usuario/', registrar_usuario, name='registro_usuario'),
    path('success/', success_page, name='success_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('carrito/', carrito, name='carrito'),
    path('agregar_al_carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar_cantidad_carrito/<int:item_id>/', actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    path('reservar-hora/', reservar_hora, name='reservar_hora'),
    path('historial/', historial, name='historial'),
]