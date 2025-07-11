# Generated by Django 5.0 on 2025-04-28 12:23

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bowls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mixes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, default=None, verbose_name='Описание')),
                ('banner', models.ImageField(blank=True, default=None, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tasteType', models.CharField(choices=[('-', '-'), ('fruit', 'фруктовый'), ('gastro', 'гастро'), ('sweet', 'сладкий'), ('grass', 'травяной'), ('fresh', 'свежий')], default='-', max_length=10, verbose_name='Тип вкуса')),
            ],
            options={
                'verbose_name': 'Микс',
                'verbose_name_plural': 'Миксы',
                'db_table': 'app_mixes',
            },
        ),
        migrations.CreateModel(
            name='MixFavorites',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Избранный микс',
                'verbose_name_plural': 'Избранные миксы',
                'db_table': 'app_mixfavorites',
            },
        ),
        migrations.CreateModel(
            name='MixLikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Лайк микса',
                'verbose_name_plural': 'Лайки миксов',
                'db_table': 'app_mixlikes',
            },
        ),
        migrations.CreateModel(
            name='MixTobacco',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('weight', models.PositiveIntegerField(verbose_name='Процент содержания табака')),
            ],
            options={
                'db_table': 'app_mixtobacco',
            },
        ),
        migrations.CreateModel(
            name='MixBowl',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bowl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mixes', to='bowls.bowls', verbose_name='Чаша')),
            ],
            options={
                'verbose_name': 'Чаша микса',
                'verbose_name_plural': 'Чаши миксов',
                'db_table': 'app_mixbowl',
            },
        ),
    ]
