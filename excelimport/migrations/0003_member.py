# Generated by Django 3.2.18 on 2024-02-02 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excelimport', '0002_alter_exceldata_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('joined_date', models.DateField(null=True)),
            ],
        ),
    ]
