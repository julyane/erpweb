# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0005_auto_20160120_2319'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoriadespesa',
            options={'ordering': ('nome',), 'verbose_name': 'Categoria de Despesa', 'verbose_name_plural': 'Categorias de Despesas'},
        ),
        migrations.AlterModelOptions(
            name='categoriareceita',
            options={'ordering': ('nome',), 'verbose_name': 'Categoria de Receita', 'verbose_name_plural': 'Categorias de Receitas'},
        ),
    ]
