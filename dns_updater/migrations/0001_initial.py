# Generated by Django 5.0.2 on 2025-05-05 23:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('domain_id', models.IntegerField(help_text='Linode Domain ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DNSRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Subdomain name (e.g., 'www' for www.example.com)", max_length=255)),
                ('record_type', models.CharField(choices=[('A', 'A Record'), ('AAAA', 'AAAA Record')], default='A', max_length=4)),
                ('ttl', models.IntegerField(default=300, help_text='Time To Live in seconds (minimum 300)', validators=[django.core.validators.MinValueValidator(300)])),
                ('current_value', models.CharField(help_text='Current IP address', max_length=255)),
                ('record_id', models.IntegerField(help_text='Linode Record ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('update_interval', models.IntegerField(default=300, help_text='Update interval in seconds (minimum 60)', validators=[django.core.validators.MinValueValidator(60)])),
                ('enabled', models.BooleanField(default=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='dns_updater.domain')),
            ],
            options={
                'unique_together': {('domain', 'name', 'record_type')},
            },
        ),
        migrations.CreateModel(
            name='UpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_value', models.CharField(max_length=255)),
                ('new_value', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='dns_updater.dnsrecord')),
            ],
        ),
    ]
