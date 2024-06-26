# Generated by Django 4.2.7 on 2024-03-29 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateTimeField(blank=True, null=True, verbose_name='Last Update')),
                ('sync_token', models.CharField(blank=True, default='', max_length=255, verbose_name='Sync Token')),
                ('page_token', models.CharField(blank=True, default='', max_length=255, verbose_name='Page Token')),
                ('name', models.CharField(max_length=255, verbose_name='Company Name')),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateTimeField(blank=True, null=True, verbose_name='Last Update')),
                ('sync_token', models.CharField(blank=True, default='', max_length=255, verbose_name='Sync Token')),
                ('page_token', models.CharField(blank=True, default='', max_length=255, verbose_name='Page Token')),
                ('name', models.CharField(max_length=255, verbose_name='Hall name')),
                ('google_calendar_id', models.CharField(blank=True, max_length=255, verbose_name='Google calendar ID')),
                ('hall_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_halls', to='calendar_app.company')),
            ],
            options={
                'verbose_name': 'Hall',
                'verbose_name_plural': 'Halls',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateTimeField(blank=True, null=True, verbose_name='Last Update')),
                ('sync_token', models.CharField(blank=True, default='', max_length=255, verbose_name='Sync Token')),
                ('page_token', models.CharField(blank=True, default='', max_length=255, verbose_name='Page Token')),
                ('google_id', models.CharField(blank=True, max_length=255, verbose_name='Event ID')),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('etag', models.CharField(blank=True, max_length=255, verbose_name='etag')),
                ('error', models.IntegerField(default=0)),
                ('event_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_events', to='calendar_app.company')),
                ('event_hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hall_events', to='calendar_app.hall')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'indexes': [models.Index(fields=['date_start', 'date_end', 'event_hall'], name='calendar_ap_date_st_c3e47e_idx')],
            },
        ),
    ]
