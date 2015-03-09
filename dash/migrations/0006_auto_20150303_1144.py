# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0005_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default=b'photos/def.jpeg', upload_to=b'photos/', verbose_name=b'Picture'),
            preserve_default=True,
        ),
    ]
