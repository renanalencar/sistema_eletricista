# Generated by Django 2.0.7 on 2018-10-26 00:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PedidoDeServico', '0029_auto_20181025_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodeservico',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 25, 21, 1, 35, 578445), verbose_name='Data da solicitação'),
        ),
    ]
