from django.contrib import admin
from .models import Category, Brand, Product, Size, ProductImage
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name_brand', 'slug_brand']
    prepopulated_fields = {'slug_brand': ('name_brand',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name_size', 'slug_size']
    prepopulated_fields = {'slug_size': ('name_size',)}


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['name', 'brand', 'category', 'price', 'available', 'image_thumbnail', 'created']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created',)

    class Meta:
        model = Product

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return ''

    image_thumbnail.short_description = 'Зображення'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass



