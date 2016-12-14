# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 10:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userlogin', '0002_auto_20160711_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='blog_author',
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_publisher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blog_publisher', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
