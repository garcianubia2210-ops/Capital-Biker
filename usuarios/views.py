from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegistroUsuarioForm


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            login(request, usuario)

            return redirect("usuarios:perfil")

        else:

            messages.error(
                request,
                "Usuario o contraseña incorrectos."
            )

    return render(
        request,
        "usuarios/login.html",
        {
            "mostrar_navbar": False,
            "mostrar_footer": False,
            "titulo": "Iniciar Sesión | Capital Biker",
        }
    )


def registro_view(request):

    if request.method == "POST":

        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            messages.success(
                request,
                "Usuario creado correctamente. Ahora puedes iniciar sesión."
            )

            return redirect(
                "usuarios:login"
            )

    else:

        form = RegistroUsuarioForm()


    return render(
        request,
        "usuarios/registro.html",
        {
            "form": form,
            "mostrar_navbar": False,
            "mostrar_footer": False,
            "titulo": "Crear cuenta | Capital Biker",
        }
    )


def perfil_view(request):

    return render(
        request,
        "usuarios/perfil.html",
        {
            "mostrar_navbar": True,
            "mostrar_footer": True,
            "titulo": "Mi Perfil | Capital Biker",
        }
    )
    