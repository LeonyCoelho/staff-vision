# Generated by Django 4.2.5 on 2023-10-19 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_efetivos', '0003_alter_preset_settings_sector_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preset_settings',
            name='sector_width',
            field=models.IntegerField(default='4'),
        ),
    ]
