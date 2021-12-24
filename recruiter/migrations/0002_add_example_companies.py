from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from recruiter.models import Company

        with transaction.atomic():
            Seeking_Alpha = Company(name="Seeking Alpha", description="This is Seeking Alpha",
                                    website_url="SeekingAlpha.com")
            Ping_Identity = Company(name="Ping Identity", description="This is Ping Identity",
                                    website_url="PingIdentity.com")
            Synamedia = Company(
                name="Synamedia", description="This is Synamedia", website_url="Synamedia.com")
            Check_Point_Software_Technologies = Company(name="Check Point Software Technologies, Ltd.",
                                                        description="This is Check Point Software Technologies, Ltd.",
                                                        website_url="Check_Point_Software_Technologies.com")
            Toptal = Company(
                name="Toptal", description="This is Toptal", website_url="Toptal.com")
            Kaplan_Open_Source = Company(name="Kaplan Open Source", description="This is Kaplan Open Source",
                                         website_url="KaplanOpenSource.com")
            Seeking_Alpha.save()
            Ping_Identity.save()
            Synamedia.save()
            Check_Point_Software_Technologies.save()
            Toptal.save()
            Kaplan_Open_Source.save()

    operations = [
        migrations.RunPython(generate_data),
    ]
