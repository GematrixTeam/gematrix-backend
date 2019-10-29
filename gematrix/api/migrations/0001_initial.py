# Generated by Django 2.2.6 on 2019-10-25 18:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Core',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='unique id', primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('sort', models.IntegerField(blank=True, default=0, verbose_name='номер объекта для сортировки')),
                ('active', models.BooleanField(db_index=True, default=True, verbose_name='активен ли объект')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='обновлен')),
            ],
            options={
                'verbose_name': 'ядро',
                'verbose_name_plural': 'ядра',
                'ordering': ('sort', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('core_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Core')),
                ('source_url', models.CharField(default='index', max_length=256, verbose_name='Адрес сайта')),
            ],
            options={
                'verbose_name': 'Источник данных',
                'verbose_name_plural': 'Источники данных',
                'ordering': ('sort', 'title'),
            },
            bases=('api.core',),
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('core_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Core')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.Producer', verbose_name='Источник данных')),
            ],
            options={
                'verbose_name': 'Датасет',
                'verbose_name_plural': 'Датасеты',
            },
            bases=('api.core',),
        ),
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('core_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Core')),
                ('x_data', models.DateField(blank=True, null=True, verbose_name='Период времени')),
                ('y_value', models.SmallIntegerField(blank=True, null=True, verbose_name='Уровень ряда')),
                ('related_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='points', to='api.Core', verbose_name='Элемент ряда')),
            ],
            options={
                'verbose_name': 'Элемент ряда',
                'verbose_name_plural': 'Элементы ряда',
            },
            bases=('api.core',),
        ),
    ]