# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0002_populate_questionnaire_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'ordering': ['name'], 'verbose_name_plural': 'Faculties'},
        ),
        migrations.AddField(
            model_name='projectoutput',
            name='title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
