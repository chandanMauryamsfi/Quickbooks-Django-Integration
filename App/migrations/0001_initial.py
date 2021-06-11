# Generated by Django 3.2.3 on 2021-06-10 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_Name', models.CharField(max_length=50)),
                ('family_Name', models.CharField(max_length=50)),
                ('qb_EmpId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PrimaryAddr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('postal_Code', models.CharField(max_length=10)),
                ('qb_Id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField()),
                ('hours', models.IntegerField()),
                ('employee_name', models.CharField(max_length=100)),
                ('qb_employee_id', models.IntegerField()),
                ('billable_Status', models.CharField(max_length=50)),
                ('hourly_Rate', models.IntegerField()),
                ('time_activity_id', models.IntegerField()),
                ('name_of', models.CharField(choices=[('Employee', 'Employee'), ('Vendor', 'Vendor')], default='Employee', max_length=10)),
                ('Employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fully_Qualified_Name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('item_id', models.IntegerField()),
                ('time', models.CharField(max_length=100)),
                ('Employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='primaryAddr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.primaryaddr'),
        ),
    ]