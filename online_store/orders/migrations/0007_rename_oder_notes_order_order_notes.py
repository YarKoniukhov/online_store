# Generated by Django 4.2.6 on 2023-11-27 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_stripe_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='oder_notes',
            new_name='order_notes',
        ),
    ]
