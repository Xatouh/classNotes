# Generated by Django 5.1.7 on 2025-06-06 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='model',
            field=models.CharField(choices=[('tiny', 'Tiny'), ('base', 'Base'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('large-v3', 'Large v3')], default='tiny', max_length=50),
        ),
    ]
