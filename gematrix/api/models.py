# Date: 25.10.2019 23:00
# Author: MaximRaduntsev


import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Core(models.Model):
    """ Базовый класс """

    class Meta:
        ordering = ('sort', 'title')
        verbose_name = _('ядро')
        verbose_name_plural = _('ядра')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique id",
                          editable=False, unique=True)
    title = models.CharField(_('название'), max_length=255, null=True)
    description = models.TextField(_('описание'), blank=True, null=True)
    sort = models.IntegerField(_('номер объекта для сортировки'), default=0, blank=True, null=False)
    active = models.BooleanField(_('активен ли объект'), default=True, db_index=True)
    created = models.DateTimeField(_('создан'), auto_now_add=True)
    updated = models.DateTimeField(_('обновлен'), auto_now=True)

    def __str__(self):
        return f'{self.title}' if self.title else ''

    def delete(self, **kwargs):
        if 'force' in kwargs:
            super().delete()
        else:
            self.is_active = False
            self.save()

    def get_verbose_name(self):
        return self._meta.verbose_name

    @classmethod
    def get_model_name(cls):
        return cls.__name__.lower()

    @classmethod
    def get_app_name(cls):
        return cls._meta.app_label.lower()

    def get_absolute_url(self):
        return reverse(f'{self.get_app_name()}:{self.get_model_name().capitalize()}Detail', args=[self.pk])

    def get_point(self):
        for point in self.points.all():
            return point


class DataPointManager(models.QuerySet):

    def get_queryset(self, **kwargs):
        return self.filter(Q(active=True) | Q(related_obj__isnull=True))

    def get_count(self):
        return self.count()


class DataPoint(Core):
    """ Класс элемента ряда """

    class Meta:
        verbose_name = _('Элемент ряда')
        verbose_name_plural = _('Элементы ряда')

    x_data = models.DateField(_('Период времени'), null=True, blank=True)
    y_value = models.SmallIntegerField(_('Уровень ряда'), null=True, blank=True)
    related_obj = models.ForeignKey(
        Core, verbose_name=_('Элемент ряда'), null=True, blank=True,
        related_name='points', on_delete=models.CASCADE)

    objects = DataPointManager.as_manager()

    @classmethod
    def get_count_all(cls):
        return cls.objects.get_count()

    def delete(self, **kwargs):
        self.related_obj = None
        super().delete(**kwargs)

    def __str__(self):
        return "%s" % self.id


class Producer(Core):
    """ Класс источника """

    class Meta:
        ordering = ('sort', 'title')
        verbose_name = _('Источник данных')
        verbose_name_plural = _('Источники данных')

    source_url = models.CharField(_('Адрес сайта'), max_length=256, blank=False,
                                  null=False, default='index')

    def get_source(self):
        attrs = ('title', 'source_url')
        attr_list = (getattr(self, attr, None) or '' for attr in attrs)
        return ' '.join(attr_list)


class Dataset(Core):
    """ Класс датасета """

    class Meta:
        verbose_name = _('Датасет')
        verbose_name_plural = _('Датасеты')

    source = models.ForeignKey(Producer, verbose_name=_('Источник данных'), null=True, blank=True,
                               related_name='products', on_delete=models.CASCADE)
