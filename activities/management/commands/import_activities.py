from django.core.management.base import BaseCommand

from activities.models import Activity


class Command(BaseCommand):

    help = "Import Activities"


    def handle(self, *args, **kwargs):

        with open("Activity List.txt") as f:

            for line in f:

                activity = line.strip()

                if activity:

                    Activity.objects.get_or_create(

                        activity_name=activity

                    )

        self.stdout.write("Activities Imported")