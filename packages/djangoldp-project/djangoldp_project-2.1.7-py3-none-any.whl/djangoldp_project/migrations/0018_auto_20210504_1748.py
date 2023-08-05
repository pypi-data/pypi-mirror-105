# Generated by Django 2.2.20 on 2021-05-04 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_project', '0017_auto_20210125_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='businessProvider',
        ),
        migrations.AddField(
            model_name='businessprovider',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='businessprovider', to='djangoldp_project.Project'),
        ),
    ]
