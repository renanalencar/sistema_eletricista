# Generated by Django 2.0.7 on 2018-10-22 19:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PedidoDeServico', '0008_auto_20181021_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodeservico',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 16, 49, 59, 824490), verbose_name='Data da solicitação'),
        ),
    ]
