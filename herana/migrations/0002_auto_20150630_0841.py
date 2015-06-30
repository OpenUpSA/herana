# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectdetail',
            options={'permissions': (('view_projectdetail', 'Can only view project details'), ('reject_projectdetail', 'Can reject the project which has been submitted'))},
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='faculty',
            field=models.ForeignKey(verbose_name=b' In which faculty/school is the project located?', to='herana.Faculty', null=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='focus_area',
            field=models.ManyToManyField(help_text=b'Select ALL applicable<br>', to='herana.FocusArea', verbose_name='In which of the following areas would you place your project?'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='focus_area_text',
            field=models.CharField(help_text=b'', max_length=256, null=True, verbose_name='If other was chosen above, please describe.'),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='strategic_objectives',
            field=models.ManyToManyField(to='herana.StrategicObjective', verbose_name='What are the 4 main strategic objectives of the project?'),
        ),
    ]
