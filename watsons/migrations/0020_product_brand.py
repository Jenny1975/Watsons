# Generated by Django 2.0 on 2019-01-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watsons', '0019_auto_20190109_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
