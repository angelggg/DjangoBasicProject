# Generated by Django 3.1.3 on 2020-12-05 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geostats', '0007_auto_20201117_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_population', models.IntegerField(default=0)),
                ('mean_elevation', models.IntegerField(default=0)),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'geostats'), ('model', 'town')), models.Q(('app_label', 'geostats'), ('model', 'region')), models.Q(('app_label', 'geostats'), ('model', 'country')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'content_type')},
            },
        ),
    ]
