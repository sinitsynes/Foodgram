import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def load_ingredients(self):
        with open(
            '../../data/ingredients.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.reader(f)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )

    def handle(self, *args, **kwargs):
        self.load_ingredients()
