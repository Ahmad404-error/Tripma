import csv
from django.core.management.base import BaseCommand
from main.models import Airline

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                try:
                    name = row.get('name', '').strip()
                    code = row.get('code', '').strip()

                    if not Airline.objects.filter(code=code).exists():
                        Airline.objects.create(
                            name=name,
                            code=code,
                            # другие поля
                        )
                    
                except Exception as e:
                    print(f"Error processing row: {row}, error: {str(e)}")

        self.stdout.write(self.style.SUCCESS('Successfully imported airlines'))