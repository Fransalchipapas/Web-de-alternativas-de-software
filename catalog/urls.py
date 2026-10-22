from django.urls import path

from . import views

urlpatterns = [
    path("", views.SearchView.as_view(), name="home"),
    path("buscar/", views.SearchView.as_view(), name="buscar"),
    path("producto/<slug:slug>/", views.ProductDetailView.as_view(), name="producto"),
]
