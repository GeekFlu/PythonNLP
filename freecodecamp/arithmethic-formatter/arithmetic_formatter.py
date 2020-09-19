import re


class Operation:
    valid_operations = ["+", "-"]
    regular_expression_find_numbers = r"([-+]*\s*\d+)"
    regular_expression_remove_spaces = r"\s+"
    regular_expression_invalid_operations = r"[/%\\*]+"

    def __init__(self, str_operation):
        self.num_list = []
        self.result = 0
        self.raw_text = str_operation

        if len(re.findall(self.regular_expression_invalid_operations, str_operation)):
            raise ValueError("Error: Operator must be '+' or '-'.")

        strip_part = re.sub(self.regular_expression_remove_spaces, "", str_operation)
        extracted_n = re.findall(self.regular_expression_find_numbers, strip_part)
        for number in extracted_n:
            try:
                n = int(number)
                if n < -9999 or n > 9999:
                    raise ValueError("Error: Numbers cannot be more than four")
            except ValueError:
                raise ValueError("Numbers must only contain digits.")

            self.num_list.append(n)

    def calculate(self):
        for n in self.num_list:
            self.result += n

    def print(self):


    def __str__(self):
        return f"Operation {self.raw_text} = {self.result}"


def arithmetic_arranger(lst, show_ans=False):
    if len(lst) > 5:
        raise ValueError("Error: Too many problems.")

    lst_operations = list()
    for operation in lst:
        op = Operation(operation)
        if show_ans:
            op.calculate()
        lst_operations.append(op)

    return lst_operations


if __name__ == "__main__":
    s = r"([-+]*\s*\d+)"
    new_s = re.sub(r"\s+", "", "   53 + 34-34    - 4545+ 3")
    invalid = re.findall(r"[/%\\*]+", "55 / 7 + 3 % 67 * 4")
    result = re.findall(s, "523 - 20 + 30 - 10")
    list_example = ["523 - 10 - 10 - 10"]
    for operation01 in arithmetic_arranger(list_example, True):
        print(operation01)
