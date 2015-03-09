# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0004_auto_20150302_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(default=b'def.jpeg', upload_to=b'photos/', verbose_name=b'Picture'),
            preserve_default=True,
        ),
    ]
