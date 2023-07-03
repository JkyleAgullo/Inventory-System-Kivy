class Inventory:
    def __init__(self, category=None, name=None, date=None, exp_date=None, orig_price=0.0, qty=0, total_price=0.0, retail_price=0.0, sales_qty=0, total_sales_amount=0.0, profit=0.0):
        self.category = category
        self.name = name
        self.date = date
        self.exp_date = exp_date
        self.orig_price = orig_price
        self.qty = qty
        self.total_price = total_price
        self.retail_price = retail_price
        self.sales_qty = sales_qty
        self.total_sales_amount = total_sales_amount
        self.profit = profit
