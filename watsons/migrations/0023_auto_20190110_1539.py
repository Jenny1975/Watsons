# Generated by Django 2.0 on 2019-01-10 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watsons', '0022_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('CO', 'Cosmetic'), ('SA', 'Snacks'), ('CR', 'Care Product'), ('FC', 'Facial Cleanser'), ('MR', 'Makeup Remover'), ('LO', 'Lotion'), ('MA', 'Mask'), ('SL', 'Sunscreen lotion'), ('MW', 'Mouthwash'), ('TP', 'Toothpaste')], default='CO', max_length=2),
        ),
    ]
