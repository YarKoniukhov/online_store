from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField('Код купону', max_length=50, unique=True)
    valid_from = models.DateTimeField('З якої дати дійсний')
    valid_to = models.DateTimeField('По яку дату дійсний')
    discount = models.IntegerField('Знижка у %',
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   help_text='Відсоткове значення (від 0 до 100)')
    active = models.BooleanField('чи є купон активним/неактивним')

    def __str__(self):
        return self.code
