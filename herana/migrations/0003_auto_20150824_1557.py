# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0002_populate_questionnaire_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orglevel1',
            options={'verbose_name': 'Level 1 Node', 'verbose_name_plural': 'Level 1 Nodes'},
        ),
        migrations.AlterModelOptions(
            name='orglevel2',
            options={'verbose_name': 'Level 2 Node', 'verbose_name_plural': 'Level 2 Nodes'},
        ),
        migrations.AlterModelOptions(
            name='orglevel3',
            options={'verbose_name': 'Level 3 Node', 'verbose_name_plural': 'Level 3 Nodes'},
        ),
        migrations.RemoveField(
            model_name='projectdetail',
            name='multi_faculty',
        ),
    ]
