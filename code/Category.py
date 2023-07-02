import Terminal

category = [
    "Category:",
    "(1) Canned Goods",
    "(2) Dairy",
    "(3) Drink",
    "(4) Fruit",
    "(5) Junk Food",
    "(6) Sweet",
    "(7) Vegetable"
]

class Category:
    def __init__(self):
        self.canned_good = 6
        self.dairy = 7
        self.drink = 6
        self.fruit = 7
        self.junk_food = 1
        self.sweet = 3
        self.vegetable = 7

    @staticmethod
    def get_category_length():
        variables = vars(Category)
        return len(variables)

    @staticmethod
    def set_get_category():
        i = 0
        while True:
            for i in range(len(category)):
                Terminal.gotoxy(15, 13+i)
                print(category[i])
            Terminal.gotoxy(15, 13 + (i+2))
            print("Select: ", end="")

            try:
                choice: int = int(input().strip())
                if 1 <= choice <= 7:
                    break
                else:
                    print("\n Please choose among the choices only", end="\n\n")
            except ValueError:
                print("\n Invalid input", end="\n\n")

        cat_choice = ""
        if choice == 1:
            cat_choice = "Canned Goods"
        elif choice == 2:
            cat_choice = "Dairy"
        elif choice == 3:
            cat_choice = "Drink"
        elif choice == 4:
            cat_choice = "Fruit"
        elif choice == 5:
            cat_choice = "Junk Food"
        elif choice == 6:
            cat_choice = "Sweet"
        elif choice == 7:
            cat_choice = "Vegetable"

        return cat_choice.upper()
