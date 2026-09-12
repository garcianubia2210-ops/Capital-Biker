from django import forms
from django.contrib.auth.models import User


class RegistroUsuarioForm(forms.Form):

    nombre = forms.CharField(
        max_length=150
    )

    email = forms.EmailField()

    password1 = forms.CharField(
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput
    )


    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        return cleaned_data


    def save(self):

        usuario = User.objects.create_user(
            username=self.cleaned_data["nombre"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"]
        )

        return usuario