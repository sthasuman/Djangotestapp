# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 08:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0003_auto_20160711_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_count', models.IntegerField()),
                ('like_blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='userlogin.Blog')),
            ],
        ),
    ]