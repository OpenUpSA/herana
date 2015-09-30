# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0003_auto_20150828_0947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collaborators',
            options={'permissions': (('view_collaborators', 'Can only view collaborators'),)},
        ),
        migrations.AlterModelOptions(
            name='coursereqdetail',
            options={'permissions': (('view_coursereqdetail', 'Can only view course requirement details'),)},
        ),
        migrations.AlterModelOptions(
            name='newcoursedetail',
            options={'permissions': (('view_newcoursedetail', 'Can only view new course details'),)},
        ),
        migrations.AlterModelOptions(
            name='phdstudent',
            options={'permissions': (('view_phdstudent', 'Can only view PHD students'),)},
        ),
        migrations.AlterModelOptions(
            name='projectfunding',
            options={'permissions': (('view_projectfunding', 'Can only view project funding'),)},
        ),
        migrations.AlterModelOptions(
            name='projectoutput',
            options={'permissions': (('view_projectoutput', 'Can only view project outputs'),)},
        ),
    ]
