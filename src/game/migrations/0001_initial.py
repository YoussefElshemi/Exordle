# Generated by Django 4.0.1 on 2022-03-01 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('radius', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='Words',
            fields=[
                ('word', models.TextField(primary_key=True, serialize=False)),
                ('last_used', models.DateField()),
                ('num_correct_guesses', models.IntegerField(default=0)),
                ('num_uses', models.IntegerField(default=0)),
                ('location', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.locations')),
            ],
        ),
    ]
