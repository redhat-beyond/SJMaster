from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('jobboard', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from jobboard.models import Region, JobTitleKeyword, City

        region_names = [
            "Central",
            "South",
            "North",
            "Tel Aviv",
            "Haifa",
            "Jerusalem"
        ]

        keywords = [
            "software",
            "engineer",
            "product",
            "automation"
        ]

        with transaction.atomic():
            for name in region_names:
                Region(name=name).save()

            City(name="Tel Aviv-Yafo", region=Region.objects.get(name="Tel Aviv")).save()
            City(name="Beersheba", region=Region.objects.get(name="South")).save()
            City(name="Rishon Leziyyon", region=Region.objects.get(name="Central")).save()
            City(name="Herziliyya", region=Region.objects.get(name="Tel Aviv")).save()

            for word in keywords:
                JobTitleKeyword(keyword=word).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
