from django.contrib import admin

from .models import Alternative, Category, Company, Product, Source

admin.site.site_header = "Alternativas"
admin.site.site_title = "Alternativas"
admin.site.index_title = "Catálogo"


class SourceInline(admin.TabularInline):
    model = Source
    extra = 1


class AlternativeInline(admin.TabularInline):
    model = Alternative
    fk_name = "alternative_to"
    autocomplete_fields = ("product",)
    extra = 1
    verbose_name = "alternativa"
    verbose_name_plural = "Alternativas de este producto"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "website")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "license")
    list_filter = ("license", "categories")
    search_fields = ("name", "description", "company__name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("company",)
    filter_horizontal = ("categories",)
    inlines = [SourceInline, AlternativeInline]


@admin.register(Alternative)
class AlternativeAdmin(admin.ModelAdmin):
    list_display = ("product", "alternative_to")
    search_fields = ("product__name", "alternative_to__name", "reason")
    autocomplete_fields = ("product", "alternative_to")


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "url")
    search_fields = ("name", "url", "product__name")
    autocomplete_fields = ("product",)
