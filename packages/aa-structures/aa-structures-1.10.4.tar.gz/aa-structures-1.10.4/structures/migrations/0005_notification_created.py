# Generated by Django 2.2.5 on 2019-12-03 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("structures", "0004_auto_20191129_0308"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=None,
                help_text="Date when this notification was first received from ESI",
                null=True,
            ),
        ),
    ]
