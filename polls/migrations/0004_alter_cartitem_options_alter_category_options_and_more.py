# Generated by Django 4.2.5 on 2023-12-07 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_category_product_image2_product_image3_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name_plural': 'Cartitem'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Product'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name_plural': 'Review'},
        ),
    ]
