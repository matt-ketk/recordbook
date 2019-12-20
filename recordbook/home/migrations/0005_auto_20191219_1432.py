# Generated by Django 3.0 on 2019-12-19 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_team_join_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='designs', to='home.Account'),
        ),
    ]
