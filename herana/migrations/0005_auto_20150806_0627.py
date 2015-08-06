# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0004_auto_20150802_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectoutput',
            old_name='title',
            new_name='output_title',
        ),
        migrations.AddField(
            model_name='projectoutput',
            name='pub_title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='is_flagged',
            field=models.BooleanField(default=False, verbose_name='Suspect'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='is_rejected',
            field=models.BooleanField(default=False, verbose_name='Rejected'),
        ),
    ]
