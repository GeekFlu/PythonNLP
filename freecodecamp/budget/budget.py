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

    def deposit(self, amount, description):
        # {"amount": amount, "description": description}
        self.ledger.append({"amount": amount, "description": description})

    def __str__(self):
        len_cat_name = len(self.category_name)
        num_stars = 30 - len_cat_name
        num_stars_by_side = int(num_stars / 2)
        stars = '*' * num_stars_by_side
        text = f"{stars}{self.category_name}{stars}\n"
        for transaction in self.ledger:
            desc = transaction['description'][0:23]
            text = text + f"{desc:23} {transaction['amount']:>6.2f}\n"
        return text


if __name__ == "__main__":
    c = Category("Food")
    c.deposit(123.34, "Food Deposit1234567890")
    c.deposit(3.34, "More food plant based")
    c.deposit(55.34, "Plant Based food 12345678")
    print(c)
