from django.core.management.base import BaseCommand
from activities.models import Faculty, Activity

FACULTIES = [
    ("12001", "Mr. M. CHINNA APPANNA"),
    ("12002", "S.CHANDRA SEKHARA RAO"),
    ("12003", "K.RAJESH"),
    ("12004", "A SATYANARAYANA"),
    ("12005", "R. SRINATH"),
    ("12006", "K RATHAIAH"),
    ("12007", "PENMETSA DIVYA NAGANJALI"),
    ("1201", "P.VENKATA RAMA RAJU"),
    ("12011", "Mr. KVN RAVI"),
    ("12013", "BH RADHIKA"),
    ("12014", "S VENKATA DURGA RAO"),
    ("1202", "S.SRINIVASU"),
    ("1205", "D. VENKATA NAGA RAJU"),
    ("1207", "G. RATNAKANTH"),
    ("1208", "S. RAVI KUMAR"),
    ("1215", "S. RAVI CHANDRA"),
    ("1218", "V. PAVAN KUMAR"),
    ("1224", "V. LEELA PRASAD"),
    ("1231", "T SUMA BHARATHI"),
    ("1235", "SASI KUMAR B"),
    ("1241", "B PADMA"),
    ("1247", "K DILEEP KUMAR"),
    ("1249", "VSN MURTHY"),
    ("1251", "D SRINIVSA RAO"),
    ("1252", "PLVD RAVI KUMAR"),
    ("1254", "M SRINIVASA RAO"),
    ("1255", "Y SABITHA"),
    ("1256", "GAKS RAJEEV KUMAR"),
    ("1257", "VINAY P"),
    ("1259", "Y YESU JYOTHI"),
    ("1260", "M BHANU RANGA RAO"),
    ("1261", "M RAGHU CHANDRA"),
    ("1262", "G RAJA RAJESWARI"),
    ("1263", "LAKSHMAJI KOTLA"),
    ("1264", "N D S S KIRAN RELANGI"),
    ("1265", "B YUGANDHAR"),
    ("1266", "K RAM BABU"),
    ("1267", "N AMULYA"),
    ("1268", "G KALI VARA PRASANNA BABU"),
    ("1269", "BODUGU VIMALA VICTORIA"),
    ("1270", "K RAMKUMAR"),
    ("1271", "MANTHENA MOUNICA DEVI"),
]

ACTIVITIES = [
    "Journal Publication",
    "Conference Paper Presentation",
    "Conference Participation",
    "Workshop Participation",
    "Seminar Participation",
    "Faculty Development Program (FDP)",
    "Internship",
    "Patent Filed",
    "Patent Published",
    "NPTEL Certification",
    "Professional Certification",
    "AI Certification",
    "Consultancy Work",
    "Editorial Board Membership",
    "Reviewer (Journal)",
    "Reviewer (Conference)",
    "Award / Recognition",
    "Book Publication",
    "Book Chapter Publication",
    "Research Grant / Project",
    "Copyright",
    "Invited Talk / Guest Lecture",
    "Resource Person",
    "Session Chair",
    "Organizing Committee",
    "Industrial Training",
    "MOOC Certification",
    "Innovation / Prototype",
    "Extension Activity",
    "Other Achievement",
]

class Command(BaseCommand):

    help = "Seed Faculty and Activity master data"

    def handle(self, *args, **kwargs):

        faculty_added = 0

        activity_added = 0

        for fid, name in FACULTIES:

            _, created = Faculty.objects.get_or_create(
                faculty_id=fid,
                defaults={
                    "faculty_name": name
                }
            )

            if created:
                faculty_added += 1

        for activity in ACTIVITIES:

            _, created = Activity.objects.get_or_create(
                activity_name=activity
            )

            if created:
                activity_added += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Added {faculty_added} faculty members and {activity_added} activities."
            )
        )