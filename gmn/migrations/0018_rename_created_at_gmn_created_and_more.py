# Generated by Django 5.0.1 on 2024-04-04 09:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gmn", "0017_alter_gmn_color"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gmn",
            old_name="created_at",
            new_name="created",
        ),
        migrations.RenameField(
            model_name="gmn",
            old_name="updated_at",
            new_name="updated",
        ),
        migrations.RenameField(
            model_name="measuringpoint",
            old_name="created_at",
            new_name="created",
        ),
        migrations.RenameField(
            model_name="measuringpoint",
            old_name="updated_at",
            new_name="updated",
        ),
    ]
