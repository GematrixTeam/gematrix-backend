# Date: 25.10.2019 23:00

import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Core(models.Model):
    class Meta:
        ordering = ('-time_created',)
        verbose_name = _('ядро')
        verbose_name_plural = _('ядра')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique id",
                          editable=False, unique=True)
    name = models.CharField(_('название'), max_length=1024, null=True, blank=True)
    description = models.TextField(_('описание'), blank=True, null=True)
    sort = models.IntegerField(_('номер объекта для сортировки'), default=0, blank=True, null=False)
    active = models.BooleanField(_('активен ли объект'), default=True, db_index=True)
    time_created = models.DateTimeField(_('создан'), auto_now_add=True)
    time_updated = models.DateTimeField(_('обновлен'), auto_now=True)

    def __str__(self):
        return f'{self.name}' if self.name else ''

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


class GematrixSource(Core):
    class Meta:
        verbose_name = _('Источник данных')
        verbose_name_plural = _('Источники данных')

    source_name = models.CharField(_('Адрес сайта'), max_length=1024, blank=False, null=False, default='index')

    def get_source(self):
        attrs = ('name', 'source_name')
        attr_list = (getattr(self, attr, None) or '' for attr in attrs)
        return ' '.join(attr_list)


class GematrixDatasets(Core):
    class Meta:
        verbose_name = _('Датасет')
        verbose_name_plural = _('Датасеты')

    source = models.ForeignKey(GematrixSource, verbose_name=_('Источник данных'), null=True, blank=True,
                               on_delete=models.CASCADE)

    @property
    def data_point(self):
        return self.gematrixdata_set.all()


class GematrixDataManager(models.Manager):

    def all_objects(self):
        return super().get_queryset()

    def get_count(self):
        return self.count()


class GematrixData(Core):
    class Meta:
        verbose_name = _('Элемент ряда')
        verbose_name_plural = _('Элементы ряда')

    x_data = models.DateField(_('Период времени'), null=True, blank=True)
    y_value = models.SmallIntegerField(_('Уровень ряда'), null=True, blank=True)

    dataset = models.ForeignKey(GematrixDatasets, verbose_name=_('Датасет'), on_delete=models.CASCADE)
    objects = GematrixDataManager()

    @classmethod
    def get_count_all(cls):
        return cls.objects.get_count()

    def __str__(self):
        return f"{self.y_value}-{self.x_data}"
