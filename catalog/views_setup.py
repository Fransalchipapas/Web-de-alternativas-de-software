from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View

User = get_user_model()


class SetupForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    setup_secret = forms.CharField(
        label="Código secreto (SETUP_SECRET)",
        required=False,
        widget=forms.PasswordInput,
        help_text="Solo si configuraste SETUP_SECRET en Render.",
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        if p1:
            validate_password(p1)
        return cleaned


class SetupView(View):
    """Crea el primer superusuario. Se desactiva cuando ya existe uno."""

    template_name = "catalog/setup.html"

    def _already_done(self):
        return User.objects.filter(is_superuser=True).exists()

    def get(self, request):
        if self._already_done():
            return render(request, self.template_name, {"done": True, "form": None})
        return render(request, self.template_name, {"done": False, "form": SetupForm()})

    def post(self, request):
        if self._already_done():
            return render(request, self.template_name, {"done": True, "form": None})

        form = SetupForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"done": False, "form": form})

        from django.conf import settings

        expected = getattr(settings, "SETUP_SECRET", "") or ""
        if expected:
            if form.cleaned_data.get("setup_secret") != expected:
                form.add_error("setup_secret", "Código secreto incorrecto.")
                return render(request, self.template_name, {"done": False, "form": form})

        User.objects.create_superuser(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        return redirect("admin:login")