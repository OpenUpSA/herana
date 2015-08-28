# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0002_populate_questionnaire_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategicobjective',
            name='is_true',
            field=models.BooleanField(default=False, verbose_name=b'Statement is true'),
        ),
        migrations.AlterField(
            model_name='institute',
            name='org_level_2_name',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='org_level_3_name',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='is_flagged',
            field=models.BooleanField(default=False, verbose_name='Flag submission as suspect'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='is_rejected',
            field=models.BooleanField(default=False, verbose_name='Reject this submission'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='rejected_detail',
            field=models.TextField(null=True, verbose_name='Reason for rejecting this submission.', blank=True),
        ),
    ]
