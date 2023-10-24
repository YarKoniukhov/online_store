# Generated by Django 4.2 on 2023-10-02 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name="Ім'я")),
                ('last_name', models.CharField(max_length=50, verbose_name='Прізвище')),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=100, verbose_name='Місто')),
                ('address', models.CharField(max_length=250, verbose_name='Адреса')),
            ],
        ),
    ]
