import csv
from django.core.management.base import BaseCommand
from main.models import Airport

class Command(BaseCommand):
    help = 'Import airports from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    iata_code = row.get('iata_code', '').strip()
                    name = row.get('name', '').strip()
                    city = row.get('city', '').strip()
                    country = row.get('country', '').strip()
                    latitude = row.get('latitude', '').strip()
                    longitude = row.get('longitude', '').strip()

                    if not iata_code or not name or not city or not longitude or not latitude:
                        continue

                    Airport.objects.create(
                        iata_code=iata_code,
                        name=name,
                        city=city,
                        country=country,
                        latitude=latitude,
                        longitude=longitude
                    )
                    
                except Exception as e:
                    print(f"Error processing row: {row}, error: {str(e)}")

        self.stdout.write(self.style.SUCCESS('Successfully imported airports'))
