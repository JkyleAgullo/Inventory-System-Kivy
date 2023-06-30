class Receipt:
    def __init__(self, product_name=None, qty=0, price=0.0, total_price=0.0):
        self.product_name = product_name
        self.qty = qty
        self.price = price
        self.total_price = total_price