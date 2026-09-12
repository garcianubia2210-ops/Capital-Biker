from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.catalogo, name="lista"),

    path(
        "producto/<int:pk>/",
        views.detalle_producto,
        name="detalle"
    ),

    path("carrito/", views.carrito_view, name="carrito"),

    path("checkout/", views.checkout_view, name="checkout"),
    
    path( "pedido-confirmado/<int:pedido_id>/",
    views.pedido_confirmado,name="pedido_confirmado"),

    path(
        "carrito/aumentar/<int:item_id>/",
        views.aumentar_cantidad,
        name="aumentar_cantidad"
    ),

    path(
        "carrito/disminuir/<int:item_id>/",
        views.disminuir_cantidad,
        name="disminuir_cantidad"
    ),

    path(
        "carrito/eliminar/<int:item_id>/", views.eliminar_item, 
        name="eliminar_item"  ),
]
