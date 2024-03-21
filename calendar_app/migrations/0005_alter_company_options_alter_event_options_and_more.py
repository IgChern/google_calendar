# Generated by Django 4.2.7 on 2024-03-21 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0004_alter_event_error'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='hall',
            options={'verbose_name': 'Hall', 'verbose_name_plural': 'Halls'},
        ),
        migrations.AlterField(
            model_name='event',
            name='google_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='Event ID'),
        ),
    ]
