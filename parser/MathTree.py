"""Module to represent mathematical expressions as a tree."""

import math

import Node
import Operator
import Value


class Expression:
    """Class to represent an expression and its corresponding tree."""

    def __init__(self, mathematical_expression=None):
        """Create a tree representation out of given expression."""
        # define all allowed operators and their corresponding priorities
        self.operator_priority = {
            "^": 1,  # power
            "*": 2,
            "/": 2,
            "%": 3,  # modulo
            "+": 4,
            "-": 4,
            "sin": 0,
            "cos": 0,
            "exp": 0  # e^(x)
        }

        # create a list containing all operator symbols to simplify lookup
        self.operator_list = list(self.operator_priority.keys())

        # compute the length of the longest operator name
        self.longest_operator_length = 0
        for op in self.operator_list:
            if len(op) > self.longest_operator_length:
                self.longest_operator_length = len(op)

        # store the mathematical expression without whitespaces
        if mathematical_expression is None:
            self.mathematical_expression = ""
        else:
            self.mathematical_expression = self.delete_white_spaces(
                mathematical_expression)

        # store the length of the encapsulated expression
        self.mathematical_expression_length = len(self.mathematical_expression)

        # create the token list
        self.token_list = self.tokenize_expression()

        # create the tree
        self.root_node = self.create_tree(self.token_list)

    def __str__(self):
        return str(self.root_node)

    def delete_white_spaces(self, expression):
        """Remove all white spaces within a given string."""
        expression_without_white_spaces = ""
        for character in expression:
            if not character.isspace():
                expression_without_white_spaces += character
        return expression_without_white_spaces

    def evaluate(self):
        return self.root_node.evaluate()

    def tokenize_expression(self):
        """Return a list of the expression's single tokens in order."""
        # list to store the expression's different tokens in order
        token_list = []
        # temporary list to construct constants or variables with
        # more than one character
        related_elements = []
        # evaluate the expression character by character
        pointer = 0
        while pointer < self.mathematical_expression_length:
            character = self.mathematical_expression[pointer]
            if character.isalpha():
                # character is the first letter of a variable or an operator,
                # therefore check the following letters to decide which case
                # applies
                related_elements.append(character)
                pointer += 1
                while pointer < self.mathematical_expression_length:
                    character = self.mathematical_expression[pointer]
                    if self.mathematical_expression[pointer].isalpha():
                        related_elements.append(character)
                        pointer += 1
                        # only check if a valid operator is found when
                        # the length of the found operator is less than
                        # or equal to the length of the longest possible
                        # operator
                        if len(related_elements) <= self.longest_operator_length:
                            actual_operator = "".join(related_elements)
                            if actual_operator in self.operator_list:
                                operator_object = self.create_operator(
                                    actual_operator)
                                token_list.append(operator_object)
                                break
                    else:
                        # the actual subset of the expression has to be a
                        # variable
                        variable = "".join(related_elements)
                        variable_object = Value.Variable(variable)
                        token_list.append(variable_object)
                        break
                # Check if the pointer has reached the end of the expression
                # while scanning letters. If so, the expression ends with
                # a variable.
                if pointer == self.mathematical_expression_length:
                    variable = "".join(related_elements)
                    variable_object = Value.Variable(variable)
                    token_list.append(variable_object)
            elif character.isdigit():
                # Character is the first digit of an integer, therefore check
                # if it contains more than one digit.
                #
                # TODO: Maybe generalize this part to support floating
                # point numbers as well.
                related_elements.append(int(character))
                pointer += 1
                while pointer < self.mathematical_expression_length:
                    if self.mathematical_expression[pointer].isdigit():
                        related_elements.append(
                            int(self.mathematical_expression[pointer])
                        )
                        pointer += 1
                    elif self.mathematical_expression[pointer].isalpha():
                        raise ValueError(
                            "A number has to be followed by either an operator or a bracket.")
                    else:
                        break

                # construct an integer out of the stored digits
                length = len(related_elements)
                constant = 0
                for digit in related_elements:
                    constant += digit * (10 ** (length - 1))
                    length -= 1

                # create an object representing the constant and insert
                # it into the list
                constant_object = Value.Constant(constant)
                token_list.append(constant_object)
            else:
                # character is a special symbol and could be a bracket or
                # a single operator
                operator_object = self.create_operator(character)
                if operator_object is None:
                    if character == "(" or character == ")":
                        token_list.append(character)
                    else:
                        raise ValueError(
                            "Expression contains unknown operators.")
                else:
                    token_list.append(operator_object)
                pointer += 1
            del related_elements[:]
        return token_list

    def create_operator(self, operator_symbol):
        """
        Match the given operator symbol to its corresponding function.

        Return None if the operator symbol is unknown.
        """
        if operator_symbol == "^":
            operator_object = Operator.Operator.erator(
                "^", lambda x, y: x ** y)
        elif operator_symbol == "*":
            operator_object = Operator.Operator("*", lambda x, y: x * y)
        elif operator_symbol == "/":
            operator_object = Operator.Operator("/", lambda x, y: x / y)
        elif operator_symbol == "%":
            operator_object = Operator.Operator("%", lambda x, y: x % y)
        elif operator_symbol == "+":
            operator_object = Operator.Operator("+", lambda x, y: x + y)
        elif operator_symbol == "-":
            operator_object = Operator.Operator("-", lambda x, y: x - y)
        elif operator_symbol == "sin":
            operator_object = Operator.Operator("sin", lambda x: math.sin(x))
        elif operator_symbol == "cos":
            operator_object = Operator.Operator("cos", lambda x: math.cos(x))
        elif operator_symbol == "exp":
            operator_object = Operator.Operator("exp", lambda x: math.exp(x))
        else:
            operator_object = None
        return operator_object

    def create_tree(self, token_list):
        """Create an expression tree out of a given token list."""
        number_open_brackets = 0
        highest_priority_index = None
        highest_priority_value = None
        # evaluate the encapsulated list token by token and search for
        # the operator with the least priority which is not nested
        if len(token_list) > 1:
            pointer = 0
            while pointer < len(token_list):
                token = token_list[pointer]
                if token == "(":
                    number_open_brackets += 1
                if token == ")":
                    number_open_brackets -= 1
                if number_open_brackets == 0:
                    if isinstance(token, Operator.Operator):
                        if highest_priority_index is None:
                            # always consider the first operator in the list as
                            # a possible operator with highest priority
                            highest_priority_value = self.operator_priority[str(
                                token)]
                            highest_priority_index = pointer
                        if highest_priority_value < self.operator_priority[str(token)]:
                            highest_priority_value = self.operator_priority[str(
                                token)]
                            highest_priority_index = pointer
                pointer += 1
            least_priority_operator = token_list[highest_priority_index]
            node = Node.Node(
                least_priority_operator,
                self.create_tree(token_list[:highest_priority_index]),
                self.create_tree(token_list[highest_priority_index + 1:])
            )
        elif len(token_list) == 1:
            if isinstance(token_list[0], Value.Value):
                return token_list[0]
        return node
        #
        # if isinstance(token, self.Operator) or token == "(":
        #     operator_list.append(token)
        # elif isinstance(token, self.Constant) or isinstance(token, self.Variable):
        #     value_list.append(token)
        # elif token == ")":
        #     if len(operator_list) <= 0:
        #         raise ValueError(
        #             "Expression contains mismatched brackets.")
        #     if operator_list[-1] == "(":
        #         if len(value_list) <= 1:
        #             operator_list.pop()
        #         else:
        #             raise ValueError(
        #                 "Expression contains mismatched brackets.")
        #     if len(operator_list) <= 0:
        #         if len(value_list) == 1:
        #             root_node.set_left_child(value_list.pop())
        #         else:
        #             raise ValueError(
        #                 "Expression contains mismatched brackets.")
        #     actual_operator = operator_list.pop()
        #     sub_node = None
        #     while actual_operator != "(":
        #         if actual_operator.is_monovalent():
        #             if len(value_list) <= 0:
        #                 raise ValueError(
        #                     "A monovalent operator misses its argument.")
        #             actual_value = value_list.pop()
        #             sub_node = Node(actual_operator, actual_value)
        #         else:
        #             if len(value_list) <= 0:
        #                 raise ValueError(
        #                     "A bivalent operator misses its arguments.")
        #             right_value = value_list.pop()
        #             # peek at the operator to the left
        #             if len(operator_list) <= 0:
        #                 raise ValueError(
        #                     "A bivalent operator misses its arguments.")
        #             left_operator = operator_list[-1]
        #             if self.operator_priority[left_operator] <= actual_operator:
        #                 if len(value_list) <= 0:
        #                     raise ValueError(
        #                         "A bivalent operator misses its arguments.")
        #                 left_value = value_list.pop()
        #                 sub_node = self.Node(
        #                     actual_operator, left_value, right_value)
        #             else:
        #                 sub_node = self.Node(actual_operator, left_value=None, right_value)
        #
        # else:
        #     raise ValueError("Token list contains unknown tokens.")
