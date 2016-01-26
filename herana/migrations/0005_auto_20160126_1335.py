# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0004_auto_20150930_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectleader',
            name='position',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectleader',
            name='staff_no',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
