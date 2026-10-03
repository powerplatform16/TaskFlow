from django.core.management.base import BaseCommand
from tasks.utils import populate_demo_data


class Command(BaseCommand):
    help = 'Seeds initial sample categories, tasks, and notes for demonstration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding demo data...'))
        populate_demo_data()
        self.stdout.write(self.style.SUCCESS('Successfully populated sample categories, tasks, and notes!'))
