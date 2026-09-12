from django.contrib import messages
from django.shortcuts import render, redirect

from catalogo.models import Carrito


def index(request):
    return render(request, 'home/index.html')


def contacto(request):
    return render(request, 'home/contacto.html')


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