"""Module to represent mathematical expressions as a tree."""
from math import cos, exp, sin
from sys import maxsize

import Node
import Operator
import Value


class Expression:
    """Class to represent an expression and its corresponding tree."""

    def __init__(self, mathematical_expression):
        """Create a tree representation out of given expression."""
        # define all allowed operators and their corresponding
        # priorities (lowest priority = 0)
        self.operator_priority = {
            "^": 4,  # power
            "*": 3,
            "/": 3,
            "%": 2,  # modulo
            "+": 1,
            "-": 1,
            "sin": 5,
            "cos": 5,
            "exp": 5  # e^(x)
        }

        # create a list containing all operator symbols to simplify lookup
        self.operator_list = list(self.operator_priority.keys())

        # compute the length of the longest operator name
        self.longest_operator_length = 0
        for op in self.operator_list:
            if len(op) > self.longest_operator_length:
                self.longest_operator_length = len(op)

        # store the mathematical expression without white spaces
        self.mathematical_expression = self.delete_white_spaces(
            mathematical_expression)

        # store the length of the encapsulated expression
        self.mathematical_expression_length = len(self.mathematical_expression)

        # create token list
        self.token_list = self.tokenize_expression()

        # create tree
        self.root_node = self.create_tree(self.token_list)

    def __str__(self):
        """Return string representation of the tree."""
        return str(self.root_node)

    def delete_white_spaces(self, expression):
        """Remove all white spaces within a given string."""
        expression_without_white_spaces = ""
        for character in expression:
            if not character.isspace():
                expression_without_white_spaces += character
        return expression_without_white_spaces

    def evaluate(self, variables=None):
        """Evaluate the tree."""
        return self.root_node.evaluate(variables)

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
                        if len(related_elements) <= \
                                self.longest_operator_length:
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
                            "A number has to be followed by either an \
                            operator or a bracket.")
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
            operator_object = Operator.Operator(
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
            operator_object = Operator.Operator("sin", lambda x: sin(x))
        elif operator_symbol == "cos":
            operator_object = Operator.Operator("cos", lambda x: cos(x))
        elif operator_symbol == "exp":
            operator_object = Operator.Operator("exp", lambda x: exp(x))
        else:
            operator_object = None
        return operator_object

    def create_tree(self, token_list):
        """Create an expression tree out of a given token list."""
        # check if the token list contains an operator
        operator_is_present = False
        for token in token_list:
            if isinstance(token, Operator.Operator):
                operator_is_present = True
                break
        # evaluate the encapsulated list token by token and search for
        # the operator with the highest priority which is not nested
        if operator_is_present:
            operator_info = []
            # collect neccessary infos to all operators in the token list
            open_brackets = 0
            pointer = 0
            while pointer < len(token_list):
                token = token_list[pointer]
                if token == "(":
                    open_brackets += 1
                elif token == ")":
                    open_brackets -= 1
                elif isinstance(token, Operator.Operator):
                    info = (
                        # the operator's index in the token list
                        pointer,
                        # the operator's depth in the tree
                        open_brackets,
                        # the operator's priority
                        self.operator_priority[str(token)]
                    )
                    operator_info.append(info)
                pointer += 1
            # filter the operator info list by the lowest operator depth
            minimum_depth = maxsize  # highest possible value of type integer
            for info in operator_info:
                if info[1] < minimum_depth:
                    minimum_depth = info[1]
            # filter the operator info list by the lowest priority
            lowest_priority_info = (None, maxsize, maxsize)
            pointer = 0
            while pointer < len(operator_info):
                info = operator_info[pointer]
                if info[1] == minimum_depth \
                        and info[2] < lowest_priority_info[2]:
                    lowest_priority_info = info
                pointer += 1
            lowest_priority_operator = token_list[lowest_priority_info[0]]
            if lowest_priority_operator.is_monovalent:
                pointer = lowest_priority_info[0] + 1
                if token_list[pointer] == "(":
                    pointer += 1
                    open_brackets = 1
                    while pointer < len(token_list):
                        if open_brackets == 0:
                            break
                        token = token_list[pointer]
                        if token == "(":
                            open_brackets += 1
                        if token == ")":
                            open_brackets -= 1
                        pointer += 1
                    self.create_tree(token_list[:lowest_priority_info[0]])
                    node = Node.Node(
                        lowest_priority_operator,
                        self.create_tree(
                            token_list[lowest_priority_info[0] + 1: pointer]
                        )
                    )
                    self.create_tree(token_list[pointer:])
                else:
                    self.create_tree(token_list[:lowest_priority_info[0]])
                    node = Node.Node(
                        lowest_priority_operator,
                        self.create_tree(
                            token_list[pointer]
                        )
                    )
                    self.create_tree(token_list[pointer + 1:])
            else:
                node = Node.Node(
                    lowest_priority_operator,
                    self.create_tree(token_list[:lowest_priority_info[0]]),
                    self.create_tree(token_list[lowest_priority_info[0] + 1:])
                )
            return node
        elif len(token_list) >= 1:
            new_token_list = []
            for token in token_list:
                if token != "(" and token != ")":
                    new_token_list.append(token)
            if len(new_token_list) == 1:
                return new_token_list[0]
            else:
                raise ValueError("Invalid input.")
