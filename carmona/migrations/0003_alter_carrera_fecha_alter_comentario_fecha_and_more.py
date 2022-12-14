# Generated by Django 4.1.2 on 2022-10-30 07:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carmona', '0002_alter_carrera_fecha_alter_comentario_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrera',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 8, 45, 46, 76475)),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 8, 45, 46, 78474)),
        ),
        migrations.AlterField(
            model_name='post',
            name='fecha_publicacion',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 30, 8, 45, 46, 75474), null=True),
        ),
        migrations.AlterField(
            model_name='puntuacion',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 8, 45, 46, 79474)),
        ),
    ]
