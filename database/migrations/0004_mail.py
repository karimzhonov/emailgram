# Generated by Django 4.0.2 on 2022-02-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_user_is_admin_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
