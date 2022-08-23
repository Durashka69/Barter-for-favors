from django.db import models
from django.contrib.auth import get_user_model

from main.choices import ScoreChoice, ProductChoice


User = get_user_model()


class Favor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    subcategory = models.ForeignKey(
        'Subcategory', related_name='favors', 
        verbose_name="Подкатегория", on_delete=models.CASCADE
    )
    photo = models.ImageField(
        upload_to='images', verbose_name='Изображение', blank=True, null=True
    )
    price = models.PositiveIntegerField(verbose_name='Цена услуги', default=0)
    is_product = models.CharField(
        verbose_name='Услуга или продукт', 
        choices=ProductChoice.choices,
        max_length=7
    )
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    @property
    def favor_raiting(self):
        if self.raiting.last():
            return sum(self.raiting.values_list('score', flat=True)) / \
                len(self.raiting.values_list('score', flat=True))
        return 0

    @property
    def sum_raiting(self):
        if self.raiting.last():
            return len(self.raiting.values_list('score', flat=True))
        return 0


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории услуг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Raiting(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rating'
    )
    score = models.PositiveSmallIntegerField(
        choices=ScoreChoice.choices, verbose_name='Оценка'
    )
    favor = models.ForeignKey(
        'Favor', on_delete=models.CASCADE, verbose_name='Услуга', related_name='raiting'
    )
    comment = models.TextField(
        verbose_name='Комментарий', blank=True, null=True
    )

    def __str__(self):
        return f'{self.score} - {self.favor}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = 'Рейтинги'


class Request_Favor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    favor = models.ForeignKey(
        Favor, on_delete=models.CASCADE, verbose_name='Услуга'
    )
    email = models.EmailField(max_length=255, default='test@gmail.com')
    phone_number = models.CharField(max_length=50, default=0)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата подачи'
    )
    # status = models.CharField(max_length=20, choices=StatusChoice.choices)
    content = models.TextField(
        blank=True, null=True, verbose_name='Содержимое заявки'
    )

    def __str__(self):
        return f'Заявка на услугу: {self.user}: {self.email} -- {self.favor}'

    class Meta:
        verbose_name = 'Заявка на услугу'
        verbose_name_plural = 'Заявки на услугу'


class Subcategory(models.Model):
    title = models.CharField(
        max_length=255, verbose_name='Название подкатегории'
    )
    description = models.TextField(verbose_name='Описание подкатегории услуг')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name='Категория', related_name='subcategory'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
