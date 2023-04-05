# Generated by Django 4.1.7 on 2023-03-18 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("asset_management", "0003_asset_category_asset_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetCategory",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="asset",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="asset_management.assetcategory",
            ),
        ),
    ]
