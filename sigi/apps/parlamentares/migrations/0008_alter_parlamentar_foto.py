# Generated by Django 4.0.4 on 2022-06-20 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0007_alter_parlamentar_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parlamentar',
            name='foto',
            field=models.ImageField(blank=True, height_field='foto_altura', upload_to='parlamentares/parlamentar/fotos', width_field='foto_largura'),
        ),
    ]
