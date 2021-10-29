# Generated by Django 3.1.6 on 2021-03-15 20:15

from django.conf import settings
from django.db import migrations

from .legacy_sql.main.main import run_sql as main_run_sql
from .legacy_sql.upgrades.main import run_sql as upgrade_run_sql

BASE_VERSION = "base"


def forwards_func(apps, schema_editor):
    Version = apps.get_model("core", "Version")

    schema_editor.execute("create table if not exists version (version text);")

    db_version = Version.objects.first()
    current_version = db_version.version if db_version else BASE_VERSION

    if current_version == BASE_VERSION:
        main_run_sql(schema_editor)
        return

    upgrade_run_sql(schema_editor, current_version)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
