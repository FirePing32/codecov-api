# Generated by Django 3.2.12 on 2023-02-20 12:45

from django.db import migrations

from utils.migrations import RiskyRunSQL


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0006_auto_20221212_1111"),
    ]

    operations = [
        RiskyRunSQL(
            'ALTER TABLE "reports_commitreport" ADD CONSTRAINT "unique_commit_id_code" UNIQUE USING INDEX unique_commit_id_code_idx;'
        ),
    ]
