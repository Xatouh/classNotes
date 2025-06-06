# Generated by Django 5.1.7 on 2025-06-06 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='input')),
                ('language', models.CharField(choices=[('es', 'Spanish'), ('en', 'English'), ('fr', 'French')], default='es', max_length=10)),
                ('preprocess', models.BooleanField(default=True)),
                ('model', models.CharField(choices=[('tiny', 'Tiny'), ('base', 'Base'), ('large', 'Large')], default='tiny', max_length=50)),
            ],
        ),
    ]
