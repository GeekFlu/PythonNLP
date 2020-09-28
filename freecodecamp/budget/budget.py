import math


def create_spend_chart(categories):
    pass


class Transaction:

    def __init__(self, description, amount):
        self.description = description
        self.amount = amount

    def __str__(self):
        return f"{self.description:23} {self.amount:>6.2f}"


class Category:

    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = list()

    def __str__(self):
        len_cat_name = len(self.category_name)
        num_stars = 30 - len_cat_name
        num_stars_by_side = int(num_stars / 2)
        stars = '*' * num_stars_by_side
        return f"{stars}{self.category_name}{stars}"


if __name__ == "__main__":
    c = Category("Food")
    print(c)
    t = Transaction("groceries", 255.788)
    print(t)
    t = Transaction("groceries 02", 255.788)
    print(t)
    t = Transaction("groceries 03", 255.788)
    print(t)
