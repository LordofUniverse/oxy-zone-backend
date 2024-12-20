# Generated by Django 3.2.4 on 2021-06-29 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('profilephoto', models.ImageField(default='default.png', upload_to='media/')),
                ('desc', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField()),
                ('addr', models.TextField()),
                ('phno', models.IntegerField()),
                ('oxyprice', models.FloatField()),
                ('foreign_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.sellers')),
            ],
        ),
    ]
