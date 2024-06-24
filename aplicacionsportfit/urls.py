from django import views
from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView
from rest_framework import routers


urlpatterns = [
    path('', index, name='index'),
    path('contacto/', contacto, name='contacto'),
    path('galeria/', galeria, name='galeria'),
    path('saborlatino/', saborlatino, name='saborlatino'),
    path('carro/', carro, name='carro'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('contacto/', contacto_view, name='contacto'),
    path('checkout/', checkout, name='checkout'),
    path('registrou/', checkout, name='registrousuario'),
    # path('registro/', register_view, name='registro'),
    path('info/<int:producto_id>/', info_producto, name='infoproducto'),
    path('quienes/', quienes_somos, name='quienes'),
    path('registro/', registrar_usuario, name='registro_usuario'),
    path('success/', success_page, name='success_page'), 
    path('logout/', LogoutView.as_view(), name='logout'),
    path('carrito/', carrito, name='carrito'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar/<int:item_id>/', actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
]