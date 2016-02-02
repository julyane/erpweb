# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangoplus.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='credito',
            field=djangoplus.db.models.fields.MoneyField(null=True, verbose_name='Cr\xe9dito', max_digits=9, decimal_places=2),
        ),
    ]
