# Generated by Django 4.2.6 on 2023-11-15 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_city_user_department_np'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department_np',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='№ Нової пошти'),
        ),
    ]
