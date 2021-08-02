from django.db import models







class Category(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='№ Категории',
        unique=True
    )
    name = models.TextField(
        verbose_name='Название категории',
        unique=True
    )
    price = models.IntegerField(
        verbose_name='Цена за ед. товара',
        default=0
    )
    sheet = models.TextField(
        verbose_name='Ссылка на гугл таблицу',
        default=''
    )
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class order(models.Model):
    order_id = models.IntegerField(
        verbose_name='ID заказа',
        default=0
    )
    order_name = models.TextField(
        verbose_name='Содержимое заказа',
    )
    order_cost = models.IntegerField(
        verbose_name='Стоимость заказа',
        default=0
    )
    order_date = models.IntegerField(
        verbose_name='Дата заказа',
        default=0
    )