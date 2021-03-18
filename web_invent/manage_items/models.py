from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус')


class Type(models.Model):
    name = models.CharField('Тип', max_length=50)


class SubType(models.Model):
    name = models.CharField('Подтип', max_length=50)
    refers_to_type = models.ForeignKey(Type, on_delete=models.CASCADE)


class LocationType(models.Model):
    name = models.CharField('Тип местоположения', max_length=50)


class Location(models.Model):
    name = models.CharField('Название местоположения', max_length=50)
    location_type = models.ForeignKey(LocationType, models.PROTECT)


class Responsible(models.Model):
    name = models.CharField('ФИО отвественного', max_length=50)


class Good(models.Model):
    name = models.CharField('Наименование', max_length=50)
    inv_number = models.CharField("Инвентарный номер", max_length=30, unique=True, blank=True)
    comment = models.TextField('Примечание', max_length=1500)
    is_on_balance = models.BooleanField('На балансе?', default=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    item_type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name='Тип')
    item_subtype = models.ForeignKey(SubType, on_delete=models.PROTECT, verbose_name='Подтип')
    place = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name='Местонахождение')
    responsible = models.ForeignKey(Responsible, on_delete=models.PROTECT,
                                    verbose_name='Ответственный')
    bought_date = models.DateField('Дата приобретения', auto_now=True)
    can_be_used = models.IntegerField('Время эксплуатации', default=5)
