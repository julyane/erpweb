# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangoplus.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('soluti', '0008_auto_20160125_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='SenhaCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servico', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Servi\xe7o')),
                ('descricao', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Descri\xe7\xe3o', blank=True)),
                ('url', djangoplus.db.models.fields.UrlField(max_length=255, verbose_name='URL', blank=True)),
                ('usuario', djangoplus.db.models.fields.CharField(max_length=255, verbose_name='Usu\xe1rio')),
                ('senha', djangoplus.db.models.fields.PasswordField(max_length=255)),
                ('cliente', djangoplus.db.models.fields.ModelChoiceField(to='soluti.Cliente')),
            ],
            options={
                'can_admin': ['Administrador', 'Gerente'],
                'verbose_name': 'Senha do Cliente',
                'can_list': ['Atendente'],
                'verbose_name_plural': 'Senhas do Cliente',
            },
        ),
    ]
