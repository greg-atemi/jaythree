# Generated by Django 5.1 on 2024-08-31 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_remove_saleitems_id_saleitems_saleitem_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='sale',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
