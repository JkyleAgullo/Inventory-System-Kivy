from datetime import date, datetime, timedelta
from Category import Category


def get_date():
    current_date = date.today()
    date_string = current_date.isoformat()
    return date_string

def get_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return current_time

def set_get_expiration_date(prod_category):
    category = Category()
    current_date = date.today()
    expiration_date = None

    if prod_category.upper() == "CANNED GOODS":
        new_month = current_date.month + category.canned_good
        if new_month > 12:
            new_month = new_month % 12
            expiration_date = current_date.replace(year=current_date.year+1, month=new_month)
        else:
            expiration_date = current_date.replace(month=new_month)

    elif prod_category.upper() == "DAIRY":
        is_exceed = False
        new_days = current_date.day + category.dairy
        if current_date.month in {1, 3, 5, 7, 8, 10, 12}:
            if new_days > 31:
                new_days = new_days % 31
                is_exceed = True
        elif current_date.month == 2:
            if new_days > 28:
                new_days = new_days % 28
                is_exceed = True
        else:
            if new_days > 30:
                new_days = new_days % 30
                is_exceed = True

        if is_exceed:
            new_month = current_date.month + 1
            if new_month > 12:
                new_month = new_month % 12
                expiration_date = current_date.replace(year=current_date.year+1, month=new_month, day=new_days)
            else:
                expiration_date = current_date.replace(month=new_month, day=new_days)
        else:
            expiration_date = current_date.replace(day=new_days)

    elif prod_category.upper() == "DRINK":
        new_month = current_date.month + category.drink
        if new_month > 12:
            new_month = new_month % 12
            expiration_date = current_date.replace(year=current_date.year+1, month=new_month)
        else:
            expiration_date = current_date.replace(month=new_month)

    elif prod_category.upper() == "FRUIT":
        is_exceed = False
        new_days = current_date.day + category.fruit
        if current_date.month in {1, 3, 5, 7, 8, 10, 12}:
            if new_days > 31:
                new_days = new_days % 31
                is_exceed = True
        elif current_date.month == 2:
            if new_days > 28:
                new_days = new_days % 28
                is_exceed = True
        else:
            if new_days > 30:
                new_days = new_days % 30
                is_exceed = True

        if is_exceed:
            new_month = current_date.month + 1
            if new_month > 12:
                new_month = new_month % 12
                expiration_date = current_date.replace(year=current_date.year + 1, month=new_month, day=new_days)
            else:
                expiration_date = current_date.replace(month=new_month, day=new_days)
        else:
            expiration_date = current_date.replace(day=new_days)

    elif prod_category.upper() == "JUNK FOOD":
        expiration_date = current_date.replace(year=current_date.year + category.junk_food)

    elif prod_category.upper() == "SWEET":
        new_month = current_date.month + category.sweet
        if new_month > 12:
            new_month = new_month % 12
            expiration_date = current_date.replace(year=current_date.year + 1, month=new_month)
        else:
            expiration_date = current_date.replace(month=new_month)

    elif prod_category.upper() == "VEGETABLE":
        is_exceed = False
        new_days = current_date.day + category.vegetable
        if current_date.month in {1, 3, 5, 7, 8, 10, 12}:
            if new_days > 31:
                new_days = new_days % 31
                is_exceed = True
        elif current_date.month == 2:
            if new_days > 28:
                new_days = new_days % 28
                is_exceed = True
        else:
            if new_days > 30:
                new_days = new_days % 30
                is_exceed = True

        if is_exceed:
            new_month = current_date.month + 1
            if new_month > 12:
                new_month = new_month % 12
                expiration_date = current_date.replace(year=current_date.year + 1, month=new_month, day=new_days)
            else:
                expiration_date = current_date.replace(month=new_month, day=new_days)
        else:
            expiration_date = current_date.replace(day=new_days)

    expiration_date_string = expiration_date.isoformat()
    return expiration_date_string