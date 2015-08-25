# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0004_auto_20150825_0738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orglevel',
            options={'ordering': ['name'], 'verbose_name': 'Org Level', 'verbose_name_plural': 'Org Levels'},
        ),
        migrations.AlterModelOptions(
            name='orglevel1',
            options={'verbose_name': 'Org Level 1', 'verbose_name_plural': 'Org Level 1'},
        ),
        migrations.AlterModelOptions(
            name='orglevel2',
            options={'verbose_name': 'Org Level 2', 'verbose_name_plural': 'Org Level 2'},
        ),
        migrations.AlterModelOptions(
            name='orglevel3',
            options={'verbose_name': 'Org Level 3', 'verbose_name_plural': 'Org Level 3'},
        ),
        migrations.AddField(
            model_name='institute',
            name='org_level_1_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='org_level_2_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='org_level_3_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='orglevel2',
            name='parent',
            field=models.ForeignKey(verbose_name=b'Org Level 1', to='herana.OrgLevel1'),
        ),
        migrations.AlterField(
            model_name='orglevel3',
            name='parent',
            field=models.ForeignKey(verbose_name=b'Org Level 2', to='herana.OrgLevel2'),
        ),
    ]
