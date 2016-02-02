# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangoplus.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0007_auto_20160122_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cidade',
            field=djangoplus.db.models.fields.ModelChoiceField(to='soluti.Cidade'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado',
            field=djangoplus.db.models.fields.ModelChoiceField(to='soluti.Estado'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='tipo_contrato',
            field=djangoplus.db.models.fields.ModelChoiceField(to='soluti.TipoContrato'),
        ),
    ]
