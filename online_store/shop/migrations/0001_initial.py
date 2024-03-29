# Generated by Django 4.2 on 2023-06-27 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='Armani', max_length=200, verbose_name='Бренд')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренди',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Категорія')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Назва')),
                ('url', models.SlugField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='Описання')),
                ('image', models.FileField(blank=True, upload_to='', verbose_name='Фото товару')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна')),
                ('available', models.BooleanField(default=True, verbose_name='Доступно')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Змінено')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.category', verbose_name='Категорія')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(default=0, verbose_name='Значення')),
            ],
            options={
                'verbose_name': 'Зірка рейтингу',
                'verbose_name_plural': 'Зірки рейтингу',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, db_index=True, max_length=30, verbose_name='Розмір одягу')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Розмір одягу',
                'verbose_name_plural': 'Розміри одягу',
                'ordering': ('size',),
            },
        ),
        migrations.CreateModel(
            name='SizeShoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, db_index=True, max_length=30, verbose_name='Розмір взуття')),
                ('url', models.SlugField(max_length=160, unique=True)),
            ],
            options={
                'verbose_name': 'Розмір взуття',
                'verbose_name_plural': 'Розміри взуття',
                'ordering': ('size',),
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я")),
                ('text', models.TextField(max_length=5000, verbose_name='Повідомлення')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.reviews', verbose_name='Батьки')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Продукт')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, verbose_name='IP адреса')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='продукт')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.ratingstar', verbose_name='зірка')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(upload_to='product_images/%Y/%m/%d')),
                ('prod_image', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sizes_clothing',
            field=models.ManyToManyField(blank=True, to='shop.size', verbose_name='Розмір одягу'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes_shoes',
            field=models.ManyToManyField(blank=True, to='shop.sizeshoes', verbose_name='Розмір взуття'),
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'url')},
        ),
    ]
