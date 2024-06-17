from django import views
from django.urls import path, include
from .views import index, contacto, galeria, registrar_usuario, saborlatino, carro, login_view, register_view, contacto_view, checkout, quienes_somos, info_producto, success_page

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
    # path('registro/', register_view, name='registro'),
    path('info/<int:producto_id>/', info_producto, name='infoproducto'),
    path('quienes/', quienes_somos, name='quienes'),
    path('registro/', registrar_usuario, name='registro_usuario'),
    path('success/', success_page, name='success_page'), 
]