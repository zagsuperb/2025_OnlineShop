# PAYMENT PROCESSORS
class PaymentProcessor:
    def pay(self, amount: float):
        raise NotImplementedError('Method "pay" is not implemented')


class CreditCardPayment(PaymentProcessor):
    def __init__(self, card_number, card_holder, cvv, expiry_date, zip_code):
        self.card_number = card_number
        self.card_holder = card_holder
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.zip_code = zip_code

    def pay(self, amount: float) -> str:
        return (f'due: {amount:.2f}, charge: {self.card_number}, {self.card_holder}, '
                f'{self.cvv}, {self.expiry_date}, {self.zip_code}')


class PayPalPayment(PaymentProcessor):
    def __init__(self, email):
        self.email = str(email)

    def pay(self, amount: float) -> str:
        return f'due: {amount:.2f}, charge: {self.email}'


class BankTransferPayment(PaymentProcessor):
    def __init__(self, account_number, account_holder: str):
        self.account_number = account_number
        self.account_holder = account_holder

    def pay(self, amount: float) -> str:
        return f'due: {amount:.2f}, charge account: {self.account_number}, {self.account_holder}'