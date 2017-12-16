# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-15 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20171214_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='主机名称')),
                ('ip', models.GenericIPAddressField(protocol='ipv4', verbose_name='IP')),
                ('port', models.IntegerField(verbose_name='端口')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=32, verbose_name='邮箱'),
        ),
    ]