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

    @staticmethod
    def sort(inventory, ascending=True):
        # bubble sort
        for i in range(len(inventory) - 1):
            for j in range(len(inventory) - i - 1):
                if inventory[j].name is not None and inventory[j + 1].name is not None:
                    if (ascending and inventory[j].name > inventory[j + 1].name) or (
                            not ascending and inventory[j].name < inventory[j + 1].name):
                        inventory[j], inventory[j + 1] = inventory[j + 1], inventory[j]

        return inventory
