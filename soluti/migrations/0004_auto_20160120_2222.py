# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0003_auto_20160120_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regiao',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='subregiao',
            name='regiao',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='transportadora',
        ),
        migrations.RemoveField(
            model_name='fornecedor',
            name='regiao',
        ),
        migrations.RemoveField(
            model_name='fornecedor',
            name='subregiao',
        ),
        migrations.DeleteModel(
            name='Regiao',
        ),
        migrations.DeleteModel(
            name='SubRegiao',
        ),
        migrations.DeleteModel(
            name='Transportadora',
        ),
    ]
