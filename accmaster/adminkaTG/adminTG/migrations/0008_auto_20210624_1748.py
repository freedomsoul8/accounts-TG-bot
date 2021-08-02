# Generated by Django 3.2.4 on 2021-06-24 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminTG', '0007_auto_20210624_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена за ед. товара'),
        ),
        migrations.AlterField(
            model_name='category',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='№ Категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.TextField(unique=True, verbose_name='Название категории'),
        ),
    ]
