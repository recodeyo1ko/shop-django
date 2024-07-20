# Generated by Django 4.1 on 2024-07-20 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'ユーザ',
                'verbose_name_plural': 'ユーザ',
                'ordering': ['-user_id'],
            },
        ),
    ]
