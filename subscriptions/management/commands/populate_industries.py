from django.core.management.base import BaseCommand
from subscriptions.models import Industry

class Command(BaseCommand):
    help = 'Populates the database with the required 10 industries'

    def handle(self, *args, **options):
        industries = [
            'e-commerce',
            'healthcare',
            'real estate',
            'education',
            'finance',
            'technology',
            'hospitality',
            'marketing',
            'legal services',
            'food and beverage'
        ]

        for name in industries:
            obj, created = Industry.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created industry: {name}'))
            else:
                self.stdout.write(f'Industry already exists: {name}')
