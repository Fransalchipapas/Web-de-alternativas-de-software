from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from catalog.models import Alternative, Product


class AlternativeTests(TestCase):
    def test_rejects_self_alternative(self):
        product = Product.objects.create(name="GIMP", slug="gimp")
        alternative = Alternative(product=product, alternative_to=product)
        with self.assertRaises(ValidationError):
            alternative.full_clean()


class SearchTests(TestCase):
    def test_exact_name_lists_alternatives(self):
        photoshop = Product.objects.create(name="Photoshop", slug="photoshop")
        gimp = Product.objects.create(name="GIMP", slug="gimp")
        Alternative.objects.create(
            product=gimp,
            alternative_to=photoshop,
            reason="Código abierto",
        )

        response = self.client.get(reverse("buscar"), {"q": "Photoshop"})

        self.assertContains(response, "GIMP")
        self.assertContains(response, "Código abierto")

    def test_htmx_returns_only_the_partial(self):
        Product.objects.create(name="GIMP", slug="gimp")

        response = self.client.get(
            reverse("buscar"),
            {"q": "gimp"},
            HTTP_HX_REQUEST="true",
        )

        self.assertNotContains(response, "<html")
        self.assertContains(response, "GIMP")

    def test_several_matches_do_not_pick_one(self):
        Product.objects.create(name="Photoshop", slug="photoshop")
        Product.objects.create(name="Photopea", slug="photopea")

        response = self.client.get(reverse("buscar"), {"q": "photo"})

        self.assertContains(response, "Photoshop")
        self.assertContains(response, "Photopea")
        self.assertContains(response, "Coincidencias")
        self.assertNotContains(response, "<h3>Alternativas</h3>")
