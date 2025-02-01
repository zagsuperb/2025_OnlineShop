import logging
from .exceptions import InvalidDiscountError

logger = logging.getLogger(__name__)

# DISCOUNTS:
class Discount:
    def apply(self, price: float) -> float:
        raise NotImplementedError('method "apply" is not implemented')


class PercentageDiscount(Discount):
    def __init__(self, percentage: float):
        if not (0 <= percentage <= 100):
            raise InvalidDiscountError('Discount % should be between 0 and 100')
        self.percentage = percentage
        logger.info(f'Discount Percentage created: {self.percentage}%')

    def apply(self, price: float) -> float:
        return price - (price / 100 * self.percentage)


class FixedAmountDiscount(Discount):
    def __init__(self, discount_fixed: float):
        if discount_fixed < 0:
            raise InvalidDiscountError('Discount can not be negative')
        self.discount_fixed = discount_fixed

    def apply(self, total_price: float) -> float:
        new_price = total_price - self.discount_fixed

        if new_price < 0:
            logger.info(f'Can not apply FixedAmountDiscount, as it exceeds the price. The new price is "0".')
            return 0
        else:
            logger.info(f'Applied FixedAmountDiscount: {self.discount_fixed}')
            return new_price