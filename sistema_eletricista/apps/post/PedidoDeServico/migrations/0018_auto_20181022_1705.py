# Generated by Django 2.0.7 on 2018-10-22 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PedidoDeServico', '0017_auto_20181022_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodeservico',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 17, 5, 24, 973405), verbose_name='Data da solicitação'),
        ),
    ]
