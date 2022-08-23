from django.db import models


class ScoreChoice(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5



class StatusChoice(models.TextChoices):
    IN_PROCESS = 'В процессе'
    APPROVED = "Подвержден"
    CANCELED =  "Отменен"
    DONE = 'Выполнен'


class ProductChoice(models.TextChoices):
    IS_PRODUCT = 'Продукт'
    IS_FAVOR = 'Услуга'
