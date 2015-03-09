# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0006_auto_20150303_1144'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Person',
        ),
    ]
