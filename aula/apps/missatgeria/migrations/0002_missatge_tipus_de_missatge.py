# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missatgeria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='missatge',
            name='tipus_de_missatge',
            field=models.CharField(max_length=250, null=True),
        ),
    ]