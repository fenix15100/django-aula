# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-14 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sortides', '0010_sortida_tipus_de_pagament'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sortida',
            name='pagament_efectiu',
        ),
        migrations.RemoveField(
            model_name='sortida',
            name='pagament_entitat_bancaria',
        ),
        migrations.RemoveField(
            model_name='sortida',
            name='pagament_online',
        ),
        migrations.AlterField(
            model_name='sortida',
            name='tipus_de_pagament',
            field=models.CharField(choices=[(b'ON', 'Online a trav\xe9s del dJau'), (b'EB', "Al caixer de l'entitat banc\xe0ria"), (b'EF', 'En efectiu')], default=b'OL', help_text='Quin ser\xe0 el tipus de pagament predominant', max_length=2),
        ),
    ]