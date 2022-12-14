# Generated by Django 4.1.2 on 2022-10-30 08:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carmona', '0003_alter_carrera_fecha_alter_comentario_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 9, 9, 24, 506368)),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 9, 9, 24, 508369)),
        ),
        migrations.AlterField(
            model_name='post',
            name='fecha_publicacion',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 30, 9, 9, 24, 505369), null=True),
        ),
        migrations.AlterField(
            model_name='puntuacion',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 9, 9, 24, 508369)),
        ),
    ]
