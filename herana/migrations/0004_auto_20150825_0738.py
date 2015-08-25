# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0003_auto_20150824_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetail',
            name='org_level_1',
            field=models.ForeignKey(to='herana.OrgLevel1', null=True),
        ),
    ]
