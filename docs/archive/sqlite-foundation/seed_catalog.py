"""Add missing agreed products without overwriting existing catalog edits."""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from kiosk.models import Product


CATALOG = (
    ('rice-bowl', 'Chicken Rice Bowl', '85.00', 'A warm campus lunch'),
    ('chicken-wrap', 'Chicken Wrap', '70.00', 'A quick savory bite'),
    ('cucumber-lemonade', 'Cucumber Lemonade', '39.50', 'A refreshing cool drink'),
    ('banana-muffin', 'Banana Muffin', '34.50', 'A soft baked snack'),
    ('cheese-bun', 'Cheese Bun', '29.50', 'A light savory snack'),
    ('granola-pack', 'Granola Pack', '24.00', 'An easy takeaway snack'),
)


class Command(BaseCommand):
    help = 'Create missing Common Table products; preserve existing IDs, prices and edits.'

    def handle(self, *args, **options):
        created_count = 0
        with transaction.atomic():
            for key, name, price, description in CATALOG:
                _, created = Product.objects.get_or_create(
                    seed_key=key,
                    defaults={
                        'name': name,
                        'price': Decimal(price),
                        'description': description,
                        'is_available': True,
                    },
                )
                created_count += int(created)
        self.stdout.write(self.style.SUCCESS(
            f'Catalog ready: {created_count} created, {len(CATALOG) - created_count} preserved.'
        ))
