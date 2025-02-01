import logging
logger = logging.getLogger(__name__)
from shop.products import Product
from shop.cart import Cart
from shop.discounts import PercentageDiscount
from shop.exceptions import InvalidPriceError, GroupLimitError, OutOfStockError, NotEnoughStockError, InvalidDiscountError


# TESTING CUSTOM ERRORS
class Testing:
    def __init__(self, prod_1, prod_2, prod_3, cart):

        print('\n===== TESTING CUSTOM ERRORS =====')
        # 1
        try:
            bad_product = Product('Invalid Product', -5, 'Should fail')
        except InvalidPriceError as e:
            logger.exception('InvalidPriceError while creating product', exc_info=True)
            print(e)
        else:
            print('[InvalidPriceError] exception did not occur when expected.')

        # 2
        try:
            bad_discount = PercentageDiscount(110)
        except InvalidDiscountError as e:
            logger.exception('InvalidDiscountError while creating discount')
            print(e)
        else:
            print('[InvalidDiscountError] exception did not occur when expected.')

        # 3
        cart_limit_test = Cart(cart_limit=2)
        try:
            cart_limit_test.add_to_cart(prod_1, 1)
            cart_limit_test.add_to_cart(prod_2, 1)
            cart_limit_test.add_to_cart(prod_3, 1)
        except GroupLimitError as e:
            logger.exception('Caught GroupLimitError while adding to cart')
            print(e)
        else:
            print('[GroupLimitError] exception did not occur when expected.')

        # 4
        try:
            cart.remove_from_cart(Product('fake item', 10, 'Not in cart'), 1)
        except OutOfStockError as e:
            logger.exception('OutOfStockError while removing item')
            print(e)
        else:
            print('[OutOfStockError] exception did not occur when expected.')

        # 5
        cart.add_to_cart(prod_2, 2)
        try:
            cart.remove_from_cart(prod_2, 3)
        except NotEnoughStockError as e:
            logger.exception('Error removing too many items from cart')
            print(e)
        else:
            print('[NotEnoughStockError] exception did not occur when expected.')

        # 6
        try:
            cart.set_discount('Not a Discount object')
        except InvalidDiscountError as e:
            logger.exception('InvalidDiscountError while setting discount')
            print(e)
        else:
            print('[InvalidDiscountError] exception did not occur when expected.')

        print('===== TESTING COMPLETED =====\n')