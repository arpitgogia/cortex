# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-12 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cortex', '0012_article_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='domain_name',
        ),
        migrations.RemoveField(
            model_name='article',
            name='source',
        ),
        migrations.AlterField(
            model_name='article',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', related_query_name='article', to='cortex.AllUrl'),
        ),
    ]