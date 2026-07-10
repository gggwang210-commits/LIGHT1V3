from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MemberSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_name', models.CharField(max_length=80)),
                ('trainer_name', models.CharField(default='김라이트', max_length=80)),
                ('goal', models.CharField(max_length=120)),
                ('discomfort_area', models.CharField(blank=True, max_length=120)),
                ('qs_score', models.FloatField(default=0)),
                ('jatc_score', models.FloatField(default=0)),
                ('form_accuracy', models.FloatField(default=0)),
                ('pain_response', models.FloatField(default=0)),
                ('rpe', models.FloatField(default=0)),
                ('route', models.CharField(choices=[('AUTO', 'AUTO'), ('REVIEW', 'REVIEW'), ('BLOCK', 'BLOCK')], default='AUTO', max_length=10)),
                ('qc_status', models.CharField(choices=[('PASS', 'PASS'), ('CHECK', 'CHECK'), ('FAIL', 'FAIL')], default='PASS', max_length=10)),
                ('memo', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at', '-qs_score']},
        ),
        migrations.CreateModel(
            name='StrategyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('category', models.CharField(max_length=80)),
                ('priority', models.CharField(default='높음', max_length=30)),
                ('status', models.CharField(default='진행 필요', max_length=40)),
                ('output', models.TextField(blank=True)),
                ('risk', models.TextField(blank=True)),
            ],
        ),
    ]
