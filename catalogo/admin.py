from django.contrib import admin

from .models import (Categoria,Color,Talla, Producto,
    VarianteProducto,Carrito,ItemCarrito,Pedido,DetallePedido,)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "marca",
        "categoria",
        "precio",
        "disponible",
        "nuevo",
        "oferta",
    )

    list_filter = (
        "categoria",
        "disponible",
        "nuevo",
        "oferta",
    )

    search_fields = (
        "nombre",
        "marca",
    )


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(VarianteProducto)
class VarianteProductoAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "color",
        "talla",
        "stock",
    )

    list_filter = (
        "color",
        "talla",
    )

    search_fields = (
        "producto__nombre",
        "color__nombre",
        "talla__nombre",
    )
    
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido 
    extra = 0
    
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "telefono",
        "metodo_pago",
        "total",
        "estado",
        "creado",
    )

    list_filter = (
        "estado",
        "metodo_pago",
        "creado",
    )

    search_fields = (
        "nombre",
        "telefono",
        "correo",
    )
    inlines = [DetallePedidoInline]

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "variante",
        "cantidad",
        "precio",
    )

    search_fields = (
        "pedido__nombre",
        "variante__producto__nombre",
    )