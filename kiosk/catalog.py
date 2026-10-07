"""Fixed original exam catalog: no database, ORM, migrations or seed step."""
from dataclasses import dataclass
from decimal import Decimal

MAX_AMOUNT = Decimal('99999999.99')
MAX_QUANTITY = 99


@dataclass(frozen=True)
class Product:
    pk: int
    seed_key: str
    name: str
    price: Decimal
    description: str
    is_available: bool = True


PRODUCTS = (
    Product(1, 'rice-bowl', 'Chicken Rice Bowl', Decimal('85.00'), 'A warm campus lunch'),
    Product(2, 'chicken-wrap', 'Chicken Wrap', Decimal('70.00'), 'A quick savory bite'),
    Product(3, 'cucumber-lemonade', 'Cucumber Lemonade', Decimal('39.50'), 'A refreshing cool drink'),
    Product(4, 'banana-muffin', 'Banana Muffin', Decimal('34.50'), 'A soft baked snack'),
    Product(5, 'cheese-bun', 'Cheese Bun', Decimal('29.50'), 'A light savory snack'),
    Product(6, 'granola-pack', 'Granola Pack', Decimal('24.00'), 'An easy takeaway snack'),
)


def available_products():
    return [product for product in PRODUCTS if product.is_available]


def find_product(identifier):
    return next((product for product in available_products() if product.pk == identifier), None)
