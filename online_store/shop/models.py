from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Brand(models.Model):
    name_brand = models.CharField(max_length=200, db_index=True)
    slug_brand = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name_brand',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self):
        return self.name_brand

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.slug_brand])


class Size(models.Model):
    name_size = models.CharField(max_length=30, db_index=True, blank=True)
    slug_size = models.SlugField(max_length=30, db_index=True, unique=True)

    class Meta:
        ordering = ('name_size',)
        verbose_name = 'Розмір'
        verbose_name_plural = 'Розміри'

    def __str__(self):
        if self.name_size:
            return self.name_size
        else:
            return 'Немає розміру'  # Возвращаем сообщение, если размер не указан

    def get_absolute_url(self):
        return reverse('shop:product_list_by_size', args=[self.slug_size])


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, blank=True)
    image = models.FileField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class ProductImage(models.Model):
    prod_image = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='product_images/%Y/%m/%d')

    def __str__(self):
        return self.prod_image.name



"""
class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.image.name
"""