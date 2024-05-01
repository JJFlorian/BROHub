# Generated by Django 5.0.4 on 2024-05-01 15:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0036_remove_personalapikey_scope"),
    ]

    operations = [
        migrations.AddField(
            model_name="personalapikey",
            name="scope",
            field=models.TextField(
                default="",
                help_text="A space-separated list of {endpoint|*}:{read|readwrite}.",
            ),
            preserve_default=False,
        ),
    ]
