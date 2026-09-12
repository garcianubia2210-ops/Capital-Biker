from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import (Categoria,Producto, VarianteProducto,
    Carrito,ItemCarrito,Pedido,DetallePedido,)

def catalogo(request):
    categorias = Categoria.objects.prefetch_related(
        "productos"
    ).all()

    return render(
        request,
        "catalogo/productos.html",
        {
            "categorias": categorias,
        }
    )


def detalle_producto(request, pk):
    producto = get_object_or_404(
        Producto.objects.prefetch_related(
            "variantes__color",
            "variantes__talla"
        ),
        pk=pk
    )

    if request.method == "POST":

        variante_id = request.POST.get("variante")
        cantidad = int(request.POST.get("cantidad", 1))

        variante = get_object_or_404(
            VarianteProducto,
            id=variante_id,
            producto=producto
        )

        if cantidad < 1:
            cantidad = 1

        if cantidad > variante.stock:
            messages.error(
                request,
                f"Solo hay {variante.stock} unidades disponibles."
            )
            return redirect(
                "catalogo:detalle",
                pk=producto.pk
            )

        carrito_id = request.session.get("carrito_id")

        if carrito_id:
            carrito = Carrito.objects.filter(
                id=carrito_id
            ).first()
        else:
            carrito = None

        if not carrito:
            carrito = Carrito.objects.create()
            request.session["carrito_id"] = carrito.id

        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            variante=variante
        )

        if creado:
            item.cantidad = cantidad

        else:
            nueva_cantidad = item.cantidad + cantidad

            if nueva_cantidad > variante.stock:
                messages.error(
                    request,
                    f"No puedes agregar más de {variante.stock} unidades."
                )
                return redirect(
                    "catalogo:detalle",
                    pk=producto.pk
                )

            item.cantidad = nueva_cantidad

        item.save()

        messages.success(
            request,
            f"{producto.nombre} fue agregado al carrito."
        )

        return redirect("catalogo:carrito")

    return render(
        request,
        "catalogo/producto_detalle.html",
        {
            "producto": producto
        }
    )


def carrito_view(request):
    carrito_id = request.session.get("carrito_id")

    carrito = None
    total = 0

    if carrito_id:
        carrito = Carrito.objects.filter(
            id=carrito_id
        ).first()

    if carrito:
        total = sum(
            item.subtotal()
            for item in carrito.items.all()
        )

    return render(
        request,
        "catalogo/carrito.html",
        {
            "carrito": carrito,
            "total": total,
        }
    )


def aumentar_cantidad(request, item_id):
    carrito_id = request.session.get("carrito_id")

    if carrito_id:
        item = ItemCarrito.objects.filter(
            id=item_id,
            carrito_id=carrito_id
        ).first()

        if item:
            if item.cantidad < item.variante.stock:
                item.cantidad += 1
                item.save()
            else:
                messages.warning(
                    request,
                    "No puedes agregar más unidades. Has alcanzado el stock disponible."
                )

    return redirect("catalogo:carrito")


def disminuir_cantidad(request, item_id):
    carrito_id = request.session.get("carrito_id")

    if carrito_id:
        item = ItemCarrito.objects.filter(
            id=item_id,
            carrito_id=carrito_id
        ).first()

        if item:
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()

    return redirect("catalogo:carrito")


def eliminar_item(request, item_id):
    carrito_id = request.session.get("carrito_id")

    if carrito_id:
        item = ItemCarrito.objects.filter(
            id=item_id,
            carrito_id=carrito_id
        ).first()

        if item:
            item.delete()

    return redirect("catalogo:carrito")


def checkout_view(request):
    carrito_id = request.session.get("carrito_id")

    carrito = None

    if carrito_id:
        carrito = Carrito.objects.filter(
            id=carrito_id
        ).first()

    # Verificar que exista el carrito y que tenga productos
    if not carrito or not carrito.items.exists():
        messages.warning(
            request,
            "Tu carrito está vacío."
        )
        return redirect("catalogo:carrito")

    # Si el cliente confirma la compra
    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        correo = request.POST.get("correo", "").strip()
        direccion = request.POST.get("direccion", "").strip()
        metodo_pago = request.POST.get("metodo_pago", "").strip()

        # Verificar que todos los datos estén completos
        if not all([
            nombre,
            telefono,
            correo,
            direccion,
            metodo_pago
        ]):
            messages.error(
                request,
                "Por favor completa todos los campos."
            )

            return render(
                request,
                "catalogo/checkout.html",
                {
                    "carrito": carrito,
                    "total": carrito.total(),
                }
            )

        # Verificar nuevamente el stock antes de crear el pedido
        for item in carrito.items.select_related(
            "variante__producto"
        ).all():

            if item.cantidad > item.variante.stock:
                messages.error(
                    request,
                    f"No hay suficiente stock para "
                    f"{item.variante.producto.nombre}."
                )

                return render(
                    request,
                    "catalogo/checkout.html",
                    {
                        "carrito": carrito,
                        "total": carrito.total(),
                    }
                )

        # Calcular total
        total = carrito.total()

        # Crear el pedido
        pedido = Pedido.objects.create(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            metodo_pago=metodo_pago,
            total=total,
        )

        # Crear los detalles y descontar stock
        for item in carrito.items.select_related(
            "variante__producto"
        ).all():

            DetallePedido.objects.create(
                pedido=pedido,
                variante=item.variante,
                cantidad=item.cantidad,
                precio=item.variante.producto.precio,
            )

            item.variante.stock -= item.cantidad
            item.variante.save()

        # Vaciar el carrito
        carrito.items.all().delete()

        # Eliminar el carrito de la sesión
        request.session.pop("carrito_id", None)

        messages.success(
            request,
            f"¡Compra realizada correctamente! "
            f"Tu pedido es el #{pedido.id}."
        )

        return redirect(
            "catalogo:pedido_confirmado",
            pedido_id=pedido.id
        )

    # Mostrar checkout
    return render(
        request,
        "catalogo/checkout.html",
        {
            "carrito": carrito,
            "total": carrito.total(),
        }
    )
    

def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(
        Pedido,
        id=pedido_id
    )

    return render(
        request,
        "catalogo/pedido_confirmado.html",
        {
            "pedido": pedido,
        }
    )
