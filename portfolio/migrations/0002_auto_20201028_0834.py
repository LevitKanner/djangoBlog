# Generated by Django 3.1.2 on 2020-10-28 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personal',
            name='tech_stack',
        ),
        migrations.AddField(
            model_name='language',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='portfolio.personal'),
            preserve_default=False,
        ),
    ]