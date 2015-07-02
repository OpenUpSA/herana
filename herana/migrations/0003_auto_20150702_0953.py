# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0002_populate_questionnaire_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetail',
            name='name',
            field=models.CharField(max_length=512, verbose_name='Please enter the name of the engagement project for which you wish to capture the details.'),
        ),
        migrations.AlterField(
            model_name='projectfunding',
            name='renewable',
            field=models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
    ]
