# Generated by Django 4.0.2 on 2022-02-23 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default=None, max_length=255)),
                ('last_name', models.CharField(default=None, max_length=255)),
                ('username', models.SlugField(default=None, max_length=255)),
                ('language_code', models.CharField(default=None, max_length=10)),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]