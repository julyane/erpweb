# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangoplus.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0002_auto_20160114_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaDespesa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', djangoplus.db.models.fields.CharField(unique=True, max_length=255, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
                'menu': ('Financeiro::CategoriaDespesa', 'fa-list'),
                'can_admin': ['Administrador'],
                'verbose_name': 'Categoria de Despesa',
                'verbose_name_plural': 'Categoria de Despesas',
            },
        ),
        migrations.CreateModel(
            name='CategoriaReceita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', djangoplus.db.models.fields.CharField(unique=True, max_length=255, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
                'menu': ('Financeiro::CategoriaReceita', 'fa-list'),
                'can_admin': ['Administrador'],
                'verbose_name': 'Categoria de Receita',
                'verbose_name_plural': 'Categoria de Receitas',
            },
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='bairro_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='bairro_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cep_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cep_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cidade_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cidade_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='classificacao',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cobranca_copiar_endereco',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='complemento_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='complemento_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='empresa_conveniada',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='endereco_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='endereco_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='entrega_copiar_endereco',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='estado_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='estado_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='pontoreferencia_cobranca',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='pontoreferencia_entrega',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='regiao',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='subregiao',
        ),
        migrations.AlterField(
            model_name='despesa',
            name='categoria',
            field=djangoplus.db.models.fields.ModelChoiceField(to='soluti.CategoriaDespesa'),
        ),
        migrations.AlterField(
            model_name='receita',
            name='categoria',
            field=djangoplus.db.models.fields.ModelChoiceField(to='soluti.CategoriaReceita'),
        ),
    ]
