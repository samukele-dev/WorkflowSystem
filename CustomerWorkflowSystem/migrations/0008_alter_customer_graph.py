# Generated by Django 3.2.20 on 2023-07-06 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerWorkflowSystem', '0007_customer_graph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='graph',
            field=models.FileField(blank=True, null=True, upload_to='graphs/'),
        ),
    ]