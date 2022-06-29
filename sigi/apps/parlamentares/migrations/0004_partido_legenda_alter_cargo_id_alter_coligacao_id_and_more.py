# Generated by Django 4.0.4 on 2022-05-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0003_auto_20210416_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='legenda',
            field=models.PositiveIntegerField(default=0, verbose_name='nº da legenda'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='coligacao',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='composicaocoligacao',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='legislatura',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mandato',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='membromesadiretora',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='mesadiretora',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='parlamentar',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='parlamentar',
            name='foto',
            field=models.ImageField(blank=True, height_field='foto_altura', upload_to='fotos/parlamentares', width_field='foto_largura'),
        ),
        migrations.AlterField(
            model_name='parlamentar',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='parlamentar',
            name='sexo',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1),
        ),
        migrations.AlterField(
            model_name='partido',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='partido',
            name='nome',
            field=models.CharField(max_length=50, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='partido',
            name='sigla',
            field=models.CharField(max_length=20, verbose_name='silga'),
        ),
        migrations.AlterField(
            model_name='sessaolegislativa',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sessaolegislativa',
            name='tipo',
            field=models.CharField(choices=[('O', 'Ordinária'), ('E', 'Extraordinária')], default='O', max_length=1),
        ),
    ]
