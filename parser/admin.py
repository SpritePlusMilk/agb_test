from django.contrib import admin

from parser import models


@admin.register(models.Source)
class Source(admin.ModelAdmin):
    list_display = ('id', 'url', 'is_active')
    search_fields = ('id', 'url')


@admin.register(models.Product)
class Product(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'quantity', 'price', 'xml_file')
    search_fields = ('id', 'name', 'category', 'quantity', 'price')


class ProductInline(admin.StackedInline):
    model = models.Product
    extra = 0


@admin.register(models.Xml)
class Xml(admin.ModelAdmin):
    list_display = ('id', 'date')
    search_fields = ('id', 'date')
    inlines = (ProductInline,)


@admin.register(models.AnalysisResponse)
class AnalysisResponse(admin.ModelAdmin):
    list_display = ('id', 'xml_file', 'text')
    search_fields = ('id', 'text')
