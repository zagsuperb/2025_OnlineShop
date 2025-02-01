import logging

logging.basicConfig(
    filename="logs.txt",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

from shop.products import Product
from shop.cart import Cart
from shop.discounts import PercentageDiscount
from shop.exceptions import InvalidPriceError, GroupLimitError, OutOfStockError, NotEnoughStockError, InvalidDiscountError
from shop.payments import CreditCardPayment, PayPalPayment, BankTransferPayment
from shop.testing import Testing

if __name__ == "__main__":

    prod_1 = Product('grapefruit', 12.5, 'big red grapefruit')
    prod_2 = Product('coconut', 44, 'mid gauge brown')
    prod_3 = Product('pineapple', 15.4, 'small bitter pineapple')
    # prod_4 = Product('banana', -7, 'curved and yellow') #testing incorrect input
    # prod_5 = Product('', 19.9, 'green fruit') #testing for incorrect input
    prod_6 = Product('watermelon', 25.5, '90% water')

    cart = Cart()

    # ADDING TO THE CART №1
    for product_try, quantity_try in [(prod_1, 3), (prod_2, 2), (prod_3, 5), (prod_6, 4)]:
        try:
            cart.add_to_cart(product_try, quantity_try)
        except ValueError as error:
            print(f'Error adding product: {error}')
        except GroupLimitError as error:
            print(error)

    # DELETING FROM THE CART
    for product_try, quantity_try in [(prod_2, 2)]:
        try:
            cart.remove_from_cart(product_try, quantity_try)
        except OutOfStockError as error:
            print(error)
        except NotEnoughStockError as error:
            print(error)

    cart2 = Cart()

    # ADDING TO THE CART №2
    for product_try, quantity_try in [(prod_1, 5), (prod_2, 1), (prod_3, 2), (prod_6, 1)]:
        try:
            cart2.add_to_cart(product_try, quantity_try)
        except ValueError as error:
            print(f'Error adding product: {error}')
        except GroupLimitError as error:
            print(error)

    ##########  HW 27/01/2025  ##########
    # ADDING CARTS
    cart += cart2

    discount = PercentageDiscount(10)
    # discount = FixedAmountDiscount(0)
    cart.set_discount(discount)
    original_total = sum(product.price * quantity for product, quantity in cart.cart.items())
    discounted_total = cart.total_price()

    # PRINING CARD
    print(cart.__str__())

    # PRINTING FINAL PRICES
    print(f'Total price before discount: {original_total:.2f}')
    print(f'Total price after discount:  {discounted_total:.2f}')
    print(f'Your savings:                {(original_total - discounted_total):.2f}\n')

    # PAYING:
    credit_card_payment = CreditCardPayment('0000-0000-0000-0000', 'John Smith', '000', '01/25', '01001')
    paypal_payment = PayPalPayment('sohn.smith@test.com')
    bank_transfer_payment = BankTransferPayment('1234567890', 'John Smith')

    print('------------------------')
    print(f'Card payment: {credit_card_payment.pay(cart.total_price())}')
    print(f'Paypal payment: {paypal_payment.pay(cart.total_price())}')
    print(f'Bank payment: {bank_transfer_payment.pay(cart.total_price())}')

    # TESTING CUSTOM ERRORS
    # Testing(prod_1, prod_2, prod_3, cart)

    #EXTRA testing HW 29/01/2025
    print('\n------------HW 29/01/2025------------')
    for product, quantity in cart:
        print(f'{product.title} * {quantity} pcs')
    print(cart.total_price())
