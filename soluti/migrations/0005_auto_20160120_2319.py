# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0004_auto_20160120_2222'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmpresaConveniada',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='credito',
        ),
    ]
