# CUSTOM EXCEPTIONS
class InvalidPriceError(Exception):
    def __init__(self, price):
        super().__init__(f'Invalid price: {price}. It should be > 0')


class InvalidDiscountError(Exception):
    def __init__(self, message):
        super().__init__(message)


class OutOfStockError(Exception):
    def __init__(self, product):
        super().__init__(f'Product "{product}" is not in the cart')


class GroupLimitError(Exception):
    def __init__(self, limit):
        super().__init__(f'The cart limit is exceeded. Maximum allowed is: {limit}')


class NotEnoughStockError(Exception):
    def __init__(self, product, available, requested):
        super().__init__(f'Cannot remove {requested} "{product.title}", only {available} left in the cart')