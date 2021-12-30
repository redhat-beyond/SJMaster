from django.contrib.auth.models import User
from django.db import migrations, transaction

from recruiter.models import Recruiter


class Migration(migrations.Migration):
    dependencies = [
        ('recruiter', '0002_add_example_companies')
    ]

    def generate_data(apps, schema_editor):
        from recruiter.models import Company

        with transaction.atomic():
            companies = [("Iron Source", "This is Iron Source", "https://www.is.com"),
                         ("Apple", "This is Apple", "https://www.apple.com"),
                         ("Microsoft", "This is Microsoft", "https://www.microsoft.com/en-il/"),
                         ("Palo Alto", "This is Palo Alto", "https://www.paloaltonetworks.com"),
                         ("Red Hat", "This is Red Hat", "https://www.redhat.com/en"),
                         ("Meta", "This is Meta", "https://about.facebook.com/meta/"),
                         ("Mobileye", "This is Mobileye", "https://www.mobileye.com/he-il/"),
                         ("Intel", "This is Intel", "https://www.intel.co.il/content/www/il/he/homepage.html"),
                         ("Elbit", "This is Elbit", "https://elbitsystems.com"),
                         ("Fiverr", "This is Fiverr", "https://www.fiverr.com"),
                         ("Amazon", "This is Amazon", "https://www.amazon.com"),
                         ("Google", "This is Google", "https://www.google.com"),
                         ("Monday", "This is Monday", "https://monday.com"),
                         ("Wix", "This is Wix", "https://www.wix.com"),
                         ("Similarweb", "This is Similarweb", "https://www.similarweb.com"),
                         ("Paypal", "This is Paypal", "https://www.paypal.com/il/home"),
                         ("Apps Flyer", "This is Apps Flyer", "https://www.appsflyer.com")]

            for name, description, website_url in companies:
                Company(name=name, description=description, website_url=website_url).save()

            users = [("1", "1_password"),
                     ("2", "2_password"),
                     ("3", "3_password"),
                     ("4", "4_password"),
                     ("5", "5_password"),
                     ("6", "6_password"),
                     ("7", "7_password"),
                     ("8", "8_password"),
                     ("9", "9_password"),
                     ("10", "10_password"),
                     ("11", "11_password"),
                     ("12", "12_password")]

            for user, password in users:
                User.objects.create_user(username=user, password=password)

            recruiters = [(User.objects.get(username='1'), 'Sivan', Company.objects.get(name="Red Hat"),
                           'Sivan@redhat.com', '050-1212121'),
                          (User.objects.get(username='2'), "Michal", Company.objects.get(name="Microsoft"),
                           "Michal@microsoft.com",
                           "050-2121211"),
                          (User.objects.get(username='3'), "Arad", Company.objects.get(name="Iron Source"),
                           "Arad@ironSource.com",
                           "050-1434343"),
                          (User.objects.get(username='4'), "Guy", Company.objects.get(name="Wix"),
                           "Guy@wix.com",
                           "050-1323456"),
                          (User.objects.get(username='5'), "Ben", Company.objects.get(name="Meta"),
                           "Ben@Meta.com",
                           "050-3232323"),
                          (User.objects.get(username='6'), "Yael", Company.objects.get(name="Red Hat"),
                           "Yael@RedHat.com",
                           "050-1212123"),
                          (User.objects.get(username='7'), "Eldar", Company.objects.get(name="Apple"),
                           "Eldar@apple.com",
                           "050-1212121"),
                          (User.objects.get(username='8'), "yarin", Company.objects.get(name="Paypal"),
                           "Yarin@paypal.com",
                           "050-1432322"),
                          (User.objects.get(username='9'), "Shani", Company.objects.get(name="Palo Alto"),
                           "Shani@PaloAlto.com",
                           "050-4343423"),
                          (User.objects.get(username='10'), "Noam", Company.objects.get(name="Intel"),
                           "Noam@intel.com",
                           "050-1212121"),
                          (User.objects.get(username='11'), "Eden", Company.objects.get(name="Amazon"),
                           "Eden@amazon.com",
                           "050-1212431"),
                          (User.objects.get(username='12'), "Din", Company.objects.get(name="Monday"),
                           "Din@monday.com",
                           "050-1432121")
                          ]

            for user, name, company, email, phone_number in recruiters:
                Recruiter(user=user, name=name, company=company, email=email, phone_number=phone_number).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
