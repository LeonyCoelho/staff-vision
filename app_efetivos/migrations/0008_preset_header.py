# Generated by Django 4.2.5 on 2023-12-13 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_efetivos', '0007_alter_preset_settings_sector_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preset_Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_width', models.IntegerField(default=12)),
                ('preset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_efetivos.dashboard_presets')),
            ],
        ),
    ]
