# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def change_difficulty_code(apps, schema_editor):

    MAPPING = {
        'VE': '0-VE',
        'E': '1-E',
        'M': '2-M',
        'H': '3-H',
        'VH': '4-VH'
    }

    Assignment = apps.get_model('assignments', 'Assignment')
    for assignment in Assignment.objects.all():
        assignment.difficulty = MAPPING[assignment.difficulty]
        assignment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_auto_20150622_1707'),
    ]

    operations = [
        migrations.RunPython(change_difficulty_code),
    ]
