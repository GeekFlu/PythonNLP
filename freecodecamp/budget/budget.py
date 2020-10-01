import math


def create_spend_chart(categories):
    """
    The chart should show the percentage spent in each category passed in to the function. The percentage spent
    should be calculated only with withdrawals and not with deposits. Down the left side of the chart should be
    labels 0 - 100. The "bars" in the bar chart should be made out of the "o" character. The height of each bar
    should be rounded down to the nearest 10. The horizontal line below the bars should go two spaces past the final
    bar. Each category name should be vertically below the bar. There should be a title at the top that says
    "Percentage spent by category".

    :param categories:
    :return:
    """


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

    def deposit(self, amount, description=""):
        """
        A deposit method that accepts an amount and description. If no description is given, it should default to an
        empty string. The method should append an object to the ledger list in the form of
        {"amount": amount, "description": description}.
        :param amount:
        :param description:
        :return:
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """
        A withdraw method that is similar to the deposit method, but the amount passed in should be stored in the ledger
        as a negative number. If there are not enough funds, nothing should be added to the ledger. This method should
        return True if the withdrawal took place, and False otherwise.
        :param amount:
        :param description:
        :return:
        """
        total = self.get_total_deposit()
        if amount < total:
            self.ledger.append({"amount": -1 * amount, "description": description})
            return True
        return False

    def get_total_deposit(self):
        total = 0
        for transaction in self.ledger:
            total = total + transaction["amount"]
        return total

    def get_balance(self):
        """
        A get_balance method that returns the current balance of the budget category based on the deposits
        and withdrawals that have occurred.
        :return:
        """
        balance = 0
        for transaction in self.ledger:
            balance = balance + transaction['amount']
        return balance

    def transfer(self, amount, category):
        """
        A transfer method that accepts an amount and another budget category as arguments. The method should add a
        withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The method should
        then add a deposit to the other budget category with the amount and the description "Transfer from [Source
        Budget Category]". If there are not enough funds, nothing should be added to either ledgers. This method
        should return True if the transfer took place, and False otherwise. :return:
        """
        are_funds = self.withdraw(amount, f"Transfer to {category.category_name}")
        if are_funds:
            category.deposit(amount, f"Transfer from {self.category_name}")
            return True
        else:
            return False

    def check_funds(self, amount):
        """
        A check_funds method that accepts an amount as an argument. It returns False if the amount is less than the
        balance of the budget category and returns True otherwise. This method should be used by both the withdraw
        method and transfer method.
        :return:
        """
        total = self.get_total_deposit()
        if amount <= total:
            return True
        else:
            return False

    def __str__(self):
        len_cat_name = len(self.category_name)
        num_stars = 30 - len_cat_name
        num_stars_by_side = int(num_stars / 2)
        stars = '*' * num_stars_by_side
        text = f"{stars}{self.category_name}{stars}\n"
        for transaction in self.ledger:
            desc = transaction['description'][0:23]
            text = text + f"{desc:23} {transaction['amount']:>4.2f}\n"

        text = text + f"Total: {self.get_total_deposit():.2f}"
        return text


if __name__ == "__main__":
    food = Category("Food")
    entretenimiento = Category("Entertainment")
    business = Category("Business")
    food.deposit(5000, "Deposito para comidas")
    entretenimiento.deposit(3000, "Dinerito para entretenimiento")
    business.deposit(2500.55, "Deposito para hacer negocios")

    food.withdraw(55.55, "Aguas y cheves")
    entretenimiento.withdraw(567.87, "Juego PS4 Ghost of TIKISHIMA??")
    business.withdraw(33.45)

    print(food)
    print(entretenimiento)
    print(business)

