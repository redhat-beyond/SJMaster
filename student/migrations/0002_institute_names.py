from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('student', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from student.models import EducationalInstitution

        institution_names = [
            "Technion - institute of Technology",
            "Hebrew University of Jerusalem",
            "Weizmann Institute of science ",
            "Bar Ilan University",
            "Tel Aviv University",
            "University of Haifa",
            "Ben Gurion University",
            "Open university",
            "Ariel University",
            "Reichman University",
            "College of law and business - Ramat Gan",
            "Academic college of Tel Aviv Yafo",
            "Afeka College of engineering, Tel Aviv",
            "Ashkelon Academic College",
            "Bezalel Academy of Art and Deisgn",
            "Center for Academic studies, Or Yehuda",
            "College of Management Academic Studies, Rishon Leziyon",
            "Dan Academic Studies",
            "Hadassah Academic College, Jerusalem",
            "Holon Institute of Technology",
            "Jerusalem Academy of Music and Dance",
            "Jerusalem College of Engineering",
            "Jerusalem College of Techonlogy",
            "Kinneret Academic College",
            "Lander Institute, Jerusalem",
            "Max Stern Academic College of Emek Yezreel",
            "Mivhar College, Bnei Brak",
            "Netanya Academic College",
            "Netanya Academic College of Law",
            "Ono Academic of College, Kiryat Ono",
            "ORT Braude college of Engineering, Karmiel",
            "Peres Academic Center, Rehovot",
            "Ruppin Academic Center",
            "Sapir Academic College",
            "Sami Shmaoon College of Engineering",
            "Sha'arei Mishpat, Hod HaSharon",
            "Shalem College, Jerusalem",
            "Shenkar College of Engineering and Design",
            "Tel Hai Academic College",
            "Westren Galilee College, Acre",
            "Yehuda Regional College, Kiryat Araba",
            "Zefat Academic College"
        ]
        with transaction.atomic():
            for name in institution_names:
                EducationalInstitution(institution_name=name).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
