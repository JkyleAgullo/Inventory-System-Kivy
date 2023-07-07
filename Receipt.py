class Receipt:
    def __init__(self, product_name=None, price=0.0, qty=0, total_price=0.0):
        self.__product_name = product_name
        self.__price = price
        self.__qty = qty
        self.__total_price = total_price

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_price(self, price):
        self.__price = price

    def set_qty(self, qty):
        self.__qty = qty

    def set_total_price(self, total_price):
        self.__total_price = total_price

    def get_product_name(self):
        return self.__product_name

    def get_price(self):
        return self.__price

    def get_qty(self):
        return self.__qty

    def get_total_price(self):
        return self.__total_price

    @staticmethod
    def sort(receipt, ascending=True):
        # bubble sort
        for i in range(len(receipt) - 1):
            for j in range(len(receipt) - i - 1):
                if (ascending and receipt[j].get_product_name() > receipt[j + 1].get_product_name()) or (
                        not ascending and receipt[j].get_product_name() < receipt[j + 1].get_product_name()):
                    receipt[j], receipt[j + 1] = receipt[j + 1], receipt[j]

        return receipt