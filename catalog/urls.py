from django.urls import path

from . import views
from .views_setup import  SetupView
urlpatterns = [
    path("", views.SearchView.as_view(), name="home"),
    path("buscar/", views.SearchView.as_view(), name="buscar"),
    path("producto/<slug:slug>/", views.ProductDetailView.as_view(), name="producto"),
    path("setup/", SetupView.as_view(), name="setup"),
]
