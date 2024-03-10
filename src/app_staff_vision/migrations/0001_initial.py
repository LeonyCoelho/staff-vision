# Generated by Django 4.2.5 on 2024-03-09 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard_Presets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preset_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('establishment_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=50)),
                ('status_color', models.CharField(default='#a5a5a5', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subSector_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_name', models.CharField(max_length=50)),
                ('theme_url', models.CharField(default='css/default.css', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id_worker', models.AutoField(primary_key=True, serialize=False)),
                ('number_w', models.IntegerField(default=0, null=True)),
                ('name_w', models.CharField(max_length=124, null=True)),
                ('observation_w', models.CharField(default='', max_length=124)),
                ('establishment_w', models.ManyToManyField(to='app_staff_vision.establishment')),
                ('position_w', models.ManyToManyField(to='app_staff_vision.position')),
                ('sector_w', models.ManyToManyField(to='app_staff_vision.sector')),
                ('shift_w', models.ManyToManyField(to='app_staff_vision.shift')),
                ('status_w', models.ManyToManyField(default='', to='app_staff_vision.status')),
                ('subSector_w', models.ManyToManyField(to='app_staff_vision.sub_sector')),
            ],
        ),
        migrations.CreateModel(
            name='Worker_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_h', models.CharField(max_length=124, null=True)),
                ('status_color_h', models.CharField(default='#a5a5a5', max_length=50)),
                ('observation_h', models.CharField(max_length=124, null=True)),
                ('date_h', models.DateField(null=True)),
                ('id_worker_h', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_staff_vision.worker')),
            ],
        ),
        migrations.CreateModel(
            name='Preset_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_position', models.IntegerField(default=0)),
                ('sector_width', models.IntegerField(default=3)),
                ('preset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_staff_vision.dashboard_presets')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_staff_vision.sector')),
            ],
        ),
        migrations.CreateModel(
            name='Preset_Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_width', models.IntegerField(default=12)),
                ('preset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_staff_vision.dashboard_presets')),
            ],
        ),
        migrations.CreateModel(
            name='Global_Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('establishment_title', models.CharField(default='Estabelecimento', max_length=50)),
                ('sector_title', models.CharField(default='Setor', max_length=50)),
                ('subSector_title', models.CharField(default='Subsetor', max_length=50)),
                ('shift_title', models.CharField(default='Turno', max_length=50)),
                ('position_title', models.CharField(default='Cargo', max_length=50)),
                ('status_title', models.CharField(default='Status', max_length=50)),
                ('logo_image', models.ImageField(null=True, upload_to='logos/uploaded_logo')),
                ('bg_image', models.ImageField(null=True, upload_to='bgs/uploaded_bgs')),
                ('institution_name', models.CharField(default='Sua Empresa', max_length=60)),
                ('theme', models.ManyToManyField(to='app_staff_vision.theme')),
            ],
        ),
        migrations.AddField(
            model_name='dashboard_presets',
            name='preset_sectors',
            field=models.ManyToManyField(to='app_staff_vision.sector'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('preset', models.ManyToManyField(to='app_staff_vision.dashboard_presets')),
                ('sector', models.ManyToManyField(to='app_staff_vision.sector')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]