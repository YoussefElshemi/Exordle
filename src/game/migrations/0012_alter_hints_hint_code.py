# Generated by Django 4.0.1 on 2022-03-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_hints_hint_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hints',
            name='hint_code',
            field=models.TextField(default=None),
        ),
    ]
