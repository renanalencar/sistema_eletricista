# Generated by Django 2.0.7 on 2018-10-22 20:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PedidoDeServico', '0020_auto_20181022_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodeservico',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 17, 6, 4, 143645), verbose_name='Data da solicitação'),
        ),
    ]
