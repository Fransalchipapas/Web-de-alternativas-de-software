from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import Alternative, Product


def search_context(query):
    query = (query or "").strip()
    products = Product.objects.none()
    selected = None
    alternatives = Alternative.objects.none()

    if query:
        products = (
            Product.objects.filter(name__icontains=query)
            .select_related("company")
            .prefetch_related("categories")
            .order_by("name")
        )
        selected = products.filter(name__iexact=query).first()
        if selected is None and len(products) == 1:
            selected = products[0]
        if selected is not None:
            alternatives = (
                Alternative.objects.filter(alternative_to=selected)
                .select_related("product", "product__company")
                .prefetch_related("product__categories")
                .order_by("product__name")
            )

    return {
        "query": query,
        "products": products,
        "selected": selected,
        "alternatives": alternatives,
    }


class SearchView(View):
    def get(self, request):
        context = search_context(request.GET.get("q", ""))
        template = "catalog/_resultados.html" if request.htmx else "catalog/search.html"
        return render(request, template, context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("company").prefetch_related(
            "categories",
            "sources",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alternatives"] = (
            Alternative.objects.filter(alternative_to=self.object)
            .select_related("product", "product__company")
            .order_by("product__name")
        )
        return context
