# Generated by Django 3.0 on 2019-12-16 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20191215_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='home.Team'),
        ),
    ]
