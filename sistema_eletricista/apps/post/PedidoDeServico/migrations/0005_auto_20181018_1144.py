# Generated by Django 2.0.7 on 2018-10-18 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PedidoDeServico', '0004_auto_20181018_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidodeservico',
            name='status',
            field=models.CharField(default='w/e', max_length=100, null=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='pedidodeservico',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 18, 11, 44, 14, 100975), verbose_name='Data da solicitação'),
        ),
    ]
