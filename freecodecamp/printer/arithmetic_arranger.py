import re


def arithmetic_arranger(lst, show_ans=False):
    if len(lst) > 5:
        return "Error: Too many problems."

    lst_operations = list()
    for operation in lst:
        try:
            op = Operation(operation)

            if show_ans:
                op.calculate()

            op.generate_printable()
            lst_operations.append(op)
        except ValueError as e:
            return e.args[0]

    printable = get_printable(lst_operations, show_ans)
    return printable


def get_printable(operations, show_ans=False):
    max_lines = 0
    for operation in operations:
        if len(operation.num_list) > max_lines:
            max_lines = len(operation.num_list)

    template = ""
    for i in range(max_lines):
        for operation in operations:
            if i < len(operation.num_list):
                template = template + operation.printable_numbers[i] + "    "
        template = template + "\n"
        template = template.rstrip("    \n")
        template = template + "\n"

    template = template.rstrip("    \n")
    template = template + "\n"

    for operation in operations:
        if show_ans:
            template = template + operation.printable_numbers[-2] + "    "
        else:
            template = template + operation.printable_numbers[-1] + "    "
    template = template.rstrip(" ")
    template = template + "\n"
    # Show Result
    for operation in operations:
        if show_ans:
            template = template + operation.printable_numbers[-1] + "    "

    template = template.rstrip("\n")
    template = template.rstrip("    ")

    return template


class Operation:
    valid_operations = ["+", "-"]
    regular_expression_find_numbers = r"([-+]*\s*\d+)"
    regular_expression_remove_spaces = r"\s+"
    regular_expression_invalid_operations = r"[/%\\*]+"

    def __init__(self, str_operation):
        self.num_list = []
        self.printable_numbers = []
        self.result = None
        self.raw_text = str_operation
        self.printable = ""

        if len(re.findall(self.regular_expression_invalid_operations, str_operation)):
            raise ValueError("Error: Operator must be '+' or '-'.")

        strip_part = re.sub(self.regular_expression_remove_spaces, "", str_operation)
        are_letters = re.findall(r"[^0-9\\+-]+", strip_part)

        if len(are_letters) > 0:
            raise ValueError("Error: Numbers must only contain digits.")

        extracted_n = re.findall(self.regular_expression_find_numbers, strip_part)
        for number in extracted_n:
            n = int(number)
            if n < -9999 or n > 9999:
                raise ValueError("Error: Numbers cannot be more than four digits.")
            self.num_list.append(n)

    def calculate(self):
        self.result = 0
        for n in self.num_list:
            self.result += n

    def generate_printable(self):
        max_number_len = len(str(max(self.num_list)))
        max_num_of_spaces = max_number_len + 1
        str_nums = [str(n) for n in self.num_list]
        operand = None
        for it, str_n in enumerate(str_nums):
            # str_n 34 and max spaces = 5  space space space 3 4
            if str_n.find('+') != -1:
                operand = '+'
                str_n = str_n.replace("+", "")
            elif str_n.find('-') != -1:
                operand = '-'
                str_n = str_n.replace("-", "")

            pre_spaces = ""
            if it == len(str_nums) - 1:
                n_range = max_num_of_spaces - len(str_n) - 1
            else:
                n_range = max_num_of_spaces - len(str_n)

            for i in range(n_range + 1):
                pre_spaces = pre_spaces + " "
            printable_number = pre_spaces + str_n
            self.printable_numbers.append(printable_number)

        if operand is None:
            operand = "+"

        self.printable_numbers[-1] = operand + self.printable_numbers[-1]

        line = ''
        for step in range(len(self.printable_numbers[-1])):
            line = line + '-'
        self.printable_numbers.append(line)

        if self.result is not None:
            s_res = str(self.result)
            spaces = ""
            for i in range(max_num_of_spaces - len(s_res)):
                spaces = spaces + " "
            self.printable_numbers.append(spaces + str(self.result))

    def __str__(self):
        return f"Operation {self.raw_text} = {self.result}"


if __name__ == "__main__":
    s = r"([-+]*\s*\d+)"
    new_s = re.sub(r"\s+", "", "   53 + 34-34    - 4545+ 3")
    invalid = re.findall(r"[/%\\*]+", "55 / 7 + 3 % 67 * 4")
    result = re.findall(s, "523 - 20 + 30 - 10")
    list_example = ["523 + 70", "12 + 33", "1 - 1"]
    operation_printable = arithmetic_arranger(list_example, True)
    print(operation_printable)
