# Generated by Django 4.1.7 on 2023-03-18 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("asset_management", "0005_assetstatus_alter_assetcategory_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("issue_date", models.DateField(verbose_name="借出日期")),
                (
                    "return_date",
                    models.DateField(blank=True, null=True, verbose_name="归还日期"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="备注")),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="asset_management.asset",
                        verbose_name="资产",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
        ),
    ]
