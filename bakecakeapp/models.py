from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        NEW = '10', _('Новый')
        SCHEDULED = '20', _('Запланирован')
        PREPARING = '30', _('Приготовление')
        DELIVERY = '40', _('Доставка'),
        COMPLETED = '50', _('Исполнен')
        CANCELLED = '90', _('Отменен')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Клиент',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='orders_used_in',
        verbose_name='Ингредиент',
        blank=True)
    writing = models.CharField(
        'Надпись',
        max_length=50,
        blank=True,
        db_index=True
    )
    comments = models.TextField('Комментарии', blank=True)
    delivery_address = models.CharField(
        'Адрес доставки',
        max_length=100,
        blank=True,
        db_index=True
    )
    delivery_time = models.DateTimeField('Время доставки', db_index=True)
    status = models.CharField(
        'Статус',
        max_length=2,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW,
        db_index=True
    )
    courier_info = models.TextField('Информация для курьера', blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    value = models.DecimalField(
        'Стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    paid = models.BooleanField(
        'Оплачен',
        db_index=True,
        default=False,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.status} {self.delivery_time}, {self.delivery_address}'


class Ingredient(models.Model):
    class Type(models.TextChoices):
        LEVELS = 'LV', _('Уровни')
        SHAPE = 'SH', _('Форма')
        TOPPING = 'TP', _('Топпинг')
        BERRIES = 'BR', _('Ягоды')
        DECOR = 'DC', _('Декор')

    name = models.CharField(
        'Название',
        max_length=30,
        db_index=True
    )
    type = models.CharField(
        'Тип',
        max_length=2,
        choices=Type.choices,
        db_index=True
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'
