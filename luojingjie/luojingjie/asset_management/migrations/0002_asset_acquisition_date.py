# Generated by Django 4.1.7 on 2023-03-18 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="acquisition_date",
            field=models.DateField(blank=True, null=True, verbose_name="采购日期"),
        ),
    ]
