# Generated by Django 4.2 on 2023-05-05 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webchatapp', '0013_alter_message_content_alter_message_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 4, 10, 23, 31, 258133, tzinfo=datetime.timezone.utc)),
        ),
    ]