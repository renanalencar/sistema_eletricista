# Generated by Django 2.0.7 on 2018-10-29 13:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PedidoDeServico', '0033_auto_20181029_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodeservico',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 10, 5, 26, 482711), verbose_name='Data da solicitação'),
        ),
    ]
