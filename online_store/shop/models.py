from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Категорія', max_length=200, db_index=True)
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.url])


class Subcategory(models.Model):
    name = models.CharField('Підкатегорія', max_length=200, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_subcategory', args=[self.url])


class Brand(models.Model):
    name = models.CharField('Бренд', max_length=200, db_index=True)
    url = models.SlugField(max_length=160, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.url])


class Product(models.Model):
    name = models.CharField('Назва', max_length=200, db_index=True)
    url = models.SlugField(max_length=200, db_index=True)
    mini_description = models.TextField('Міні опис', blank=True)
    description = models.TextField('Описання', blank=True)
    specification = models.TextField('Спосіб застосування', blank=True)
    category = models.ForeignKey(Category, verbose_name='Категорія', related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, verbose_name='Підкатегорія', on_delete=models.CASCADE,
                                    null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE)
    image = models.FileField('Фото товару', blank=True)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2)
    available = models.BooleanField('Доступно', default=True)
    created = models.DateTimeField('Створено', auto_now_add=True)
    updated = models.DateTimeField('Змінено', auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'url'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.url])


class ProductImage(models.Model):
    prod_image = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='product_images/%Y/%m/%d')

    def __str__(self):
        return self.prod_image.name


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField('Значення', default=0)

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'

    def __str__(self):
        return self.value


class Rating(models.Model):
    ip = models.CharField('IP адреса', max_length=20)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='зірка')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.star} - {self.product}'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=100)
    text = models.TextField('Повідомлення', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Батьки', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

    def __str__(self):
        return f'{self.name} - {self.product}'
