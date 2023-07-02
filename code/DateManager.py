from datetime import date, time, datetime, timedelta
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
        expiration_date = current_date.replace(month=current_date.month + category.canned_good)
    elif prod_category.upper() == "DAIRY":
        expiration_date = current_date + timedelta(days=category.dairy)
    elif prod_category.upper() == "DRINK":
        expiration_date = current_date.replace(month=current_date.month + category.drink)
    elif prod_category.upper() == "FRUIT":
        expiration_date = current_date + timedelta(days=category.fruit)
    elif prod_category.upper() == "JUNK FOOD":
        expiration_date = current_date.replace(year=current_date.year + category.junk_food)
    elif prod_category.upper() == "SWEET":
        expiration_date = current_date.replace(month=current_date.month + category.sweet)
    elif prod_category.upper() == "VEGETABLE":
        expiration_date = current_date + timedelta(days=category.vegetable)

    expiration_date_string = expiration_date.isoformat()
    return expiration_date_string