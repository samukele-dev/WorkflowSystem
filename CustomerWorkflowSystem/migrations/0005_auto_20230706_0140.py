# Generated by Django 3.2.20 on 2023-07-05 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerWorkflowSystem', '0004_alter_financialdata_expenses'),
    ]

    operations = [
        migrations.RenameField(
            model_name='financialdata',
            old_name='expenses',
            new_name='Expenses',
        ),
        migrations.RenameField(
            model_name='financialdata',
            old_name='income',
            new_name='Income',
        ),
        migrations.RenameField(
            model_name='financialdata',
            old_name='month',
            new_name='Month',
        ),
    ]
