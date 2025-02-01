import logging
from .products import Product
from .discounts import Discount
from .exceptions import GroupLimitError, OutOfStockError, NotEnoughStockError, InvalidDiscountError
logger = logging.getLogger(__name__)

# DISCOUNT-mixin:
class DiscountMixin(Discount):
    def __init__(self):
        self.discount = None

    def apply_discount(self, total: float) -> float:
        if not isinstance(self.discount, Discount):
            return total
        discounted_price = self.discount.apply(total)
        logger.info(f'Applied {self.discount.__class__.__name__}: {self.discount}. The new total: {discounted_price:.2f}')
        return discounted_price


# CART
class Cart(DiscountMixin):
    def __init__(self, cart_limit=30):
        super().__init__()
        self.cart = {}
        self.cart_limit = cart_limit
        logger.info(f'Cart created. limit: {cart_limit} products max.')

    def __iter__(self):
        for product, quantity in self.cart.items():
            yield product, quantity

    def __iadd__(self, other):
        if not isinstance(other, Cart):
            raise TypeError('Only another instance of Cart can be added')
        total_quantity = sum(self.cart.values()) + sum(other.cart.values())
        if total_quantity > self.cart_limit:
            logger.warning(f"Can't merge carts. The cart limit is exceeded ({self.cart_limit} items max).")
            raise GroupLimitError(self.cart_limit)

        for product, quantity in other.cart.items():
            self.cart[product] = self.cart.get(product, 0) + quantity

        logger.info('Carts merging was successful')
        return self

    def add_to_cart(self, product: Product, quantity: int = 1):
        if not isinstance(product, Product) or not isinstance(quantity, int) or quantity < 1:
            logger.error(f'Invalid product or quantity: {product}, {quantity}')
            raise ValueError('Invalid product or quantity')
        if sum(self.cart.values()) + quantity >= self.cart_limit and product not in self.cart:
            logger.warning(f'The cart limit is exceeded: {self.cart_limit} items.')
            raise GroupLimitError(self.cart_limit)

        self.cart[product] = self.cart.get(product, 0) + quantity
        logger.info(f'{quantity} of {product.title} was added to the cart')

    def remove_from_cart(self, product: Product, quantity: int = 1) -> bool:
        if product not in self.cart:
            logger.warning(f'Attempted to remove non-existent product: {product.title}')
            raise OutOfStockError(product)
        if not isinstance(quantity, int) or quantity < 1:
            logger.error(f'Incorrect quantity to remove: {quantity}')
            raise ValueError('Incorrect quantity to remove')
        if self.cart[product] < quantity:
            logger.warning(f'Not enough in the cart to remove: {quantity} of {product.title}, '
                            f'only {self.cart[product]} available')
            raise NotEnoughStockError(product, self.cart[product], quantity)

        self.cart[product] -= quantity
        if self.cart[product] <= 0:
            del self.cart[product]
        logger.info(f'Removed {quantity} of {product.title} from cart')
        return True

    def total_price(self) -> float:
        return self.apply_discount(sum(product.price * quantity for product, quantity in self))

    def set_discount(self, discount: Discount):
        if not isinstance(discount, Discount):
            raise InvalidDiscountError('Invalid discount type. Must be an instance of Discount.')
        self.discount = discount
        logger.info(f'Discount applied: {discount.__class__.__name__} - {discount}')

    def empty_cart(self) -> None:
        self.cart = {}

    def __str__(self) -> str:
        if not self.cart:
            return 'The cart is empty'
        cart_content = '\n'.join(f'{product.title:<15} x {quantity:<2} = {product.price * quantity:.2f}'
                                 for product, quantity in self.cart.items())
        return f'===== CART CONTENT =====\n{cart_content}\n========================'
