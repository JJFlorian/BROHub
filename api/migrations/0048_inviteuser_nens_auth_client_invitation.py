# Generated by Django 5.0.4 on 2024-08-08 13:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0047_remove_inviteuser_nens_auth_client_invitation"),
        ("nens_auth_client", "0005_alter_invitation_help_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="inviteuser",
            name="nens_auth_client_invitation",
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text="Do not fill in this one.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="nens_auth_client.invitation",
            ),
        ),
    ]
