# Generated by Django 5.0.2 on 2024-03-23 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pages.category'),
            preserve_default=False,
        ),
    ]