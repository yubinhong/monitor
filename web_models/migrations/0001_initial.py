# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 09:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CPUInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.FloatField()),
                ('system', models.FloatField()),
                ('nice', models.FloatField()),
                ('idle', models.FloatField()),
                ('iowait', models.FloatField()),
                ('steal', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='主机名')),
                ('ip_addr', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('host_alive_check_interval', models.IntegerField(default=30, verbose_name='主机存活状态检测间隔')),
                ('status', models.IntegerField(choices=[(1, 'online'), (2, 'down'), (3, 'Unreachable'), (4, 'Problem')], default=1, verbose_name='状态')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '主机',
                'verbose_name': '主机',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='主机组名')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '主机组',
                'verbose_name': '主机组',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('key', models.CharField(max_length=100)),
                ('data_type', models.CharField(choices=[('float', 'Float'), ('str', 'Str'), ('int', 'Int')], default='int', max_length=50, verbose_name='指标数据类型')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '监控指标',
                'verbose_name': '监控指标',
            },
        ),
        migrations.CreateModel(
            name='MemoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MemTotal', models.IntegerField()),
                ('MemFree', models.IntegerField()),
                ('MemUsage', models.IntegerField()),
                ('MemUsage_p', models.IntegerField()),
                ('Buffers', models.IntegerField()),
                ('Cached', models.IntegerField()),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_models.Host')),
            ],
        ),
        migrations.CreateModel(
            name='MonitorGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='监控组名')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '监控组',
                'verbose_name': '监控组',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitor_type', models.CharField(choices=[('agent', 'Agent'), ('snmp', 'SNMP')], max_length=50)),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='服务名称')),
                ('interval', models.IntegerField(default=30, verbose_name='监控间隔')),
                ('memo', models.CharField(blank=True, max_length=128, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '服务',
                'verbose_name': '服务',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='类型名称')),
                ('plugin', models.CharField(max_length=100, verbose_name='插件名')),
            ],
            options={
                'verbose_name_plural': '服务类型',
                'verbose_name': '服务类型',
            },
        ),
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='模版名称')),
                ('services', models.ManyToManyField(to='web_models.Services', verbose_name='服务列表')),
            ],
            options={
                'verbose_name_plural': '配置模版',
                'verbose_name': '配置模版',
            },
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='触发器名称')),
                ('serverity', models.CharField(choices=[('1', 'unknow'), ('2', 'warning'), ('3', 'error'), ('4', 'critical')], max_length=64, verbose_name='告警级别')),
                ('operator_type', models.CharField(choices=[('eq', '='), ('lt', '<'), ('gt', '>')], max_length=64, verbose_name='运算符')),
                ('data_calc_func', models.CharField(choices=[('avg', 'Average'), ('max', 'Max'), ('hit', 'Hit'), ('last', 'Last')], max_length=64, verbose_name='数据处理方式')),
                ('threshold', models.IntegerField(verbose_name='阀值')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_models.Items', verbose_name='关联监控指标')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_models.ServiceType', verbose_name='关联服务类型')),
            ],
            options={
                'verbose_name_plural': '触发器',
                'verbose_name': '触发器',
            },
        ),
        migrations.AddField(
            model_name='templates',
            name='trigger',
            field=models.ManyToManyField(blank=True, to='web_models.Trigger', verbose_name='关联触发器'),
        ),
        migrations.AddField(
            model_name='services',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_models.ServiceType', verbose_name='服务类型'),
        ),
        migrations.AddField(
            model_name='monitorgroup',
            name='templates',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='web_models.Templates'),
        ),
        migrations.AddField(
            model_name='host',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='web_models.HostGroup', verbose_name='所属主机组'),
        ),
        migrations.AddField(
            model_name='host',
            name='monitor_groups',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='web_models.MonitorGroup', verbose_name='所属监控组'),
        ),
        migrations.AddField(
            model_name='cpuinfo',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_models.Host'),
        ),
    ]
