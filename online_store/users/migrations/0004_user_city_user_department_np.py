# Generated by Django 4.2.6 on 2023-11-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Місто'),
        ),
        migrations.AddField(
            model_name='user',
            name='department_np',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='№ Нова пошта'),
        ),
    ]
