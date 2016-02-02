# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import soluti.models
import djangoplus.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0006_auto_20160121_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcedenciaCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', djangoplus.db.models.fields.CharField(unique=True, max_length=255, verbose_name='Descri\xe7\xe3o')),
            ],
            options={
                'ordering': ('descricao',),
                'menu': 'Clientes::Proced\xeancia dos Clientes',
                'can_admin': ['Administrador'],
                'verbose_name': 'Proced\xeancia do Cliente',
                'verbose_name_plural': 'Proced\xeancia dos Clientes',
            },
        ),
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', djangoplus.db.models.fields.CharField(unique=True, max_length=255, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
                'menu': ('Clientes::Tipos de Contratos', 'fa-list'),
                'can_admin': ['Administrador'],
                'verbose_name': 'Tipo de Contrato',
                'verbose_name_plural': 'Tipos de Contratos',
            },
        ),
        migrations.CreateModel(
            name='TipoInteracao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', djangoplus.db.models.fields.CharField(unique=True, max_length=255, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
                'menu': ('Atendimento::Tipos de Intera\xe7\xf5es', 'fa-list'),
                'can_admin': ['Administrador'],
                'verbose_name': 'Tipo de Intera\xe7\xe3o',
                'verbose_name_plural': 'Tipos de Intera\xe7\xf5es',
            },
        ),
        migrations.AlterField(
            model_name='cliente',
            name='procedencia',
            field=djangoplus.db.models.fields.ModelChoiceField(blank=True, to='soluti.ProcedenciaCliente', null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=djangoplus.db.models.fields.PhoneField9(max_length=255, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone2',
            field=djangoplus.db.models.fields.PhoneField9(max_length=255, verbose_name='Outro Telefone', blank=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='tipo_contrato',
            field=djangoplus.db.models.fields.CharField(max_length=255, verbose_name=soluti.models.TipoContrato),
        ),
        migrations.AlterField(
            model_name='lead',
            name='procedencia',
            field=djangoplus.db.models.fields.CharField(max_length=255, null=True, verbose_name=soluti.models.ProcedenciaCliente, blank=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='tipo_interacao',
            field=djangoplus.db.models.fields.CharField(max_length=255, verbose_name=soluti.models.TipoInteracao),
        ),
    ]
