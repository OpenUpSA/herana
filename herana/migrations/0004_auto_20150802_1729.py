# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herana', '0003_auto_20150729_0750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectdetail',
            options={'verbose_name': 'Engagement project', 'verbose_name_plural': 'Engagement projects', 'permissions': (('view_projectdetail', 'Can only view project details'), ('reject_projectdetail', 'Can reject the project which has been submitted'))},
        ),
        migrations.RenameField(
            model_name='projectdetail',
            old_name='date_created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='projectdetail',
            old_name='rejected',
            new_name='is_rejected',
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative',
            field=models.CharField(max_length=1, null=True, verbose_name='A3.2: Have any of the findings / results / outcomes of the project been used to implement or develop new products / services / interventions / policies?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_party',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Who implemented or developed these new products / services / interventions / policies?', choices=[(1, 'A third party has been contracted to develop the product / service / intervention / policy'), (2, 'The project team will develop the product / service / intervention / policy'), (3, 'Other')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='new_initiative_party_text',
            field=models.TextField(null=True, verbose_name='Please provide the name of the third party or describe how the product / service / intervention / policy was developed and / or implemented', blank=True),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='public_domain',
            field=models.CharField(help_text=b'If yes, please provide the URL', max_length=1, null=True, verbose_name='A2.4: Are the project proposal, written up findings of the project available electronically in the public domain?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
        ),
        migrations.AlterField(
            model_name='projectdetail',
            name='rejected_detail',
            field=models.TextField(null=True, blank=True),
        ),
    ]
