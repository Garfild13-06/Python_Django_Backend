# Generated by Django 5.0 on 2025-04-28 12:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mixes', '0001_initial'),
        ('tastecategories', '0001_initial'),
        ('tobaccos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='mixes',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mixes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mixes',
            name='categories',
            field=models.ManyToManyField(related_name='mixes', to='tastecategories.tastecategories'),
        ),
        migrations.AddField(
            model_name='mixbowl',
            name='mix',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bowl', to='mixes.mixes', verbose_name='Микс'),
        ),
        migrations.AddField(
            model_name='mixfavorites',
            name='mix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='mixes.mixes', verbose_name='Микс'),
        ),
        migrations.AddField(
            model_name='mixfavorites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='mixlikes',
            name='mix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='mixes.mixes', verbose_name='Микс'),
        ),
        migrations.AddField(
            model_name='mixlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='mixtobacco',
            name='mix',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compares', to='mixes.mixes', verbose_name='Микс'),
        ),
        migrations.AddField(
            model_name='mixtobacco',
            name='tobacco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compares', to='tobaccos.tobaccos', verbose_name='Табак'),
        ),
    ]
