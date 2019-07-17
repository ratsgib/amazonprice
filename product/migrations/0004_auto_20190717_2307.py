# Generated by Django 2.2.3 on 2019-07-17 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20190717_0234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ['created_date']},
        ),
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='product.Product'),
        ),
    ]
