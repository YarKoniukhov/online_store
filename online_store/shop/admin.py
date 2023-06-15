from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Rating, RatingStar, Reviews, Subcategory
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'category']
    prepopulated_fields = {'url': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
    prepopulated_fields = {'url': ('name',)}


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['name', 'brand', 'category', 'price', 'available', 'image_thumbnail', 'created']
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'url': ('name',)}
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


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'text', 'parent', 'product']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['ip', 'star', 'product']


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ['value']
