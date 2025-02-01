import logging
from .exceptions import InvalidPriceError
logger = logging.getLogger(__name__)

# PRODUCTS
class Product:
    def __init__(self, title: str, price: float, description: str):

        self.title = title.strip()
        if not self.title:
            raise ValueError('Title must be a non-empty string.')

        if not isinstance(price, (float, int)) or price <= 0:
            raise InvalidPriceError(price)
        if not isinstance(description, str) or not description.strip():
            raise ValueError('Description should be a not-empty string')

        self.price = float(price)
        self.description = description.strip()

        logger.info(f'Product created: {self.title} | price: {self.price} | description: {self.description}')

    def __str__(self) -> str:
        return f'{self.title}: {self.price:.2f} - {self.description}'