# Generated by Django 3.2 on 2021-08-13 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jumbotron',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_home', models.BooleanField(default=False)),
                ('en_content', models.CharField(max_length=200, verbose_name='Content in English')),
                ('zh_hans_content', models.CharField(max_length=200, verbose_name='Content in Chinese')),
                ('es_content', models.CharField(max_length=200, verbose_name='Content in Spanish')),
                ('ar_content', models.CharField(max_length=200, verbose_name='Content in Arabic')),
                ('fr_content', models.CharField(max_length=200, verbose_name='Content in French')),
                ('ru_content', models.CharField(max_length=200, verbose_name='Content in Russian')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='category.category')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='topic.topic')),
            ],
            options={
                'db_table': 'jumbotron',
                'ordering': ('-pk',),
            },
        ),
    ]
