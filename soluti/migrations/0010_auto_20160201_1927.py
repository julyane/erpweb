# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import djangoplus.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0009_senhacliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='administrador',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='administrativo',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='atendente',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='gerente',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='suporte',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='vendedor',
            name='empresa',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='vendedor',
            field=djangoplus.db.models.fields.ModelChoiceField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='responsavel',
            field=djangoplus.db.models.fields.ModelChoiceField(verbose_name='Respons\xe1vel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='interacaoticket',
            name='responsavel',
            field=djangoplus.db.models.fields.ModelChoiceField(verbose_name='Respons\xe1vel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lead',
            name='vendedor',
            field=djangoplus.db.models.fields.ModelChoiceField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='propostavenda',
            name='vendedor',
            field=djangoplus.db.models.fields.ModelChoiceField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='responsaveis',
            field=djangoplus.db.models.fields.MultipleModelChoiceField(help_text='Selecione um ou mais respons\xe1veis', to=settings.AUTH_USER_MODEL, verbose_name='Respons\xe1veis'),
        ),
        migrations.DeleteModel(
            name='Administrador',
        ),
        migrations.DeleteModel(
            name='Administrativo',
        ),
        migrations.DeleteModel(
            name='Atendente',
        ),
        migrations.DeleteModel(
            name='Gerente',
        ),
        migrations.DeleteModel(
            name='Suporte',
        ),
        migrations.DeleteModel(
            name='Vendedor',
        ),
    ]
