from django.core.exceptions import ValidationError
from django.db import models


class Company(models.Model):
    name = models.CharField("nombre", max_length=120, unique=True)
    website = models.URLField("sitio", blank=True)
    description = models.TextField("descripción", blank=True)

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("nombre", max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    class License(models.TextChoices):
        OPEN_SOURCE = "open_source", "Código abierto"
        FREE = "free", "Gratis"
        FREEMIUM = "freemium", "Freemium"
        PAID = "paid", "Pago"
        PROPRIETARY = "proprietary", "Propietario"

    name = models.CharField("nombre", max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    company = models.ForeignKey(
        Company,
        verbose_name="empresa",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name="categorías",
        blank=True,
        related_name="products",
    )
    website = models.URLField("sitio", blank=True)
    description = models.TextField("descripción", blank=True)
    license = models.CharField(
        "licencia",
        max_length=20,
        choices=License.choices,
        blank=True,
    )

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Alternative(models.Model):
    """`product` es la alternativa. `alternative_to` es el programa que reemplaza."""

    product = models.ForeignKey(
        Product,
        verbose_name="alternativa",
        on_delete=models.CASCADE,
        related_name="alternatives_out",
    )
    alternative_to = models.ForeignKey(
        Product,
        verbose_name="es alternativa de",
        on_delete=models.CASCADE,
        related_name="alternatives_in",
    )
    reason = models.TextField("por qué", blank=True)

    class Meta:
        verbose_name = "alternativa"
        verbose_name_plural = "alternativas"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "alternative_to"],
                name="unique_alternative_pair",
            ),
            models.CheckConstraint(
                condition=~models.Q(product=models.F("alternative_to")),
                name="alternative_not_self",
            ),
        ]

    def clean(self):
        if self.product_id and self.product_id == self.alternative_to_id:
            raise ValidationError("Un producto no puede ser alternativa de sí mismo.")

    def __str__(self):
        return f"{self.product} es alternativa de {self.alternative_to}"


class Source(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="producto",
        on_delete=models.CASCADE,
        related_name="sources",
    )
    name = models.CharField("nombre", max_length=120)
    url = models.URLField("enlace")

    class Meta:
        verbose_name = "fuente"
        verbose_name_plural = "fuentes"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.product})"
