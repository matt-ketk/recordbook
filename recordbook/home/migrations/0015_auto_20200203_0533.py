# Generated by Django 3.0.2 on 2020-02-03 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_design_designfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='designFile',
            field=models.CharField(default='N/A', max_length=250),
        ),
    ]
