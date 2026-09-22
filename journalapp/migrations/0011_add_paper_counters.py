from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journalapp', '0010_bookvolume_alter_researchpaper_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchpaper',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='researchpaper',
            name='download_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
