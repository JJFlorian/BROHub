# Generated by Django 5.0.1 on 2024-02-20 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gmw", "0002_rename_delivery_location_gmw_ground_level_position_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gmw",
            name="delivered_vertical_postition",
        ),
        migrations.AddField(
            model_name="gmw",
            name="deliverd_location",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
