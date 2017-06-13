"""Module to represent mathematical expressions as a tree."""

import math
from inspect import signature
from numbers import Number


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
        self.token_list = self.analyze_parts_of_expression()

        print(self.token_list)
        for token in self.token_list:
            print(token)

        # create the tree
        # self.root_node = self.create_tree()

    def delete_white_spaces(self, expression):
        """Remove all white spaces within a given string."""
        expression_without_white_spaces = ""
        for character in expression:
            if not character.isspace():
                expression_without_white_spaces += character
        return expression_without_white_spaces

    def analyze_parts_of_expression(self):
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
                        variable_object = self.Variable(variable)
                        token_list.append(variable_object)
                        break
                # Check if the pointer has reached the end of the expression
                # while scanning letters. If so, the expression ends with
                # a variable.
                if pointer == self.mathematical_expression_length:
                    variable = "".join(related_elements)
                    variable_object = self.Variable(variable)
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
                constant_object = self.Constant(constant)
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
            operator_object = self.Operator("^", lambda x, y: x ** y)
        elif operator_symbol == "*":
            operator_object = self.Operator("*", lambda x, y: x * y)
        elif operator_symbol == "/":
            operator_object = self.Operator("/", lambda x, y: x / y)
        elif operator_symbol == "%":
            operator_object = self.Operator("%", lambda x, y: x % y)
        elif operator_symbol == "+":
            operator_object = self.Operator("+", lambda x, y: x + y)
        elif operator_symbol == "-":
            operator_object = self.Operator("-", lambda x, y: x - y)
        elif operator_symbol == "sin":
            operator_object = self.Operator("sin", lambda x: math.sin(x))
        elif operator_symbol == "cos":
            operator_object = self.Operator("cos", lambda x: math.cos(x))
        elif operator_symbol == "exp":
            operator_object = self.Operator("exp", lambda x: math.exp(x))
        else:
            operator_object = None
        return operator_object

    def create_tree(self):
        """Create an expression tree out of a given token list."""
        operator_list = []
        value_list = []

        root_node = self.Node()

        # evaluate the encapsulated list token by token
        for token in self.token_list:
            if isinstance(token, self.Operator) or token == "(":
                operator_list.append(token)
            elif isinstance(token, self.Constant) or isinstance(token, self.Variable):
                value_list.append(token)
            elif token == ")":
                if len(operator_list) <= 0:
                    raise ValueError(
                        "Expression contains mismatched brackets.")
                if operator_list[-1] == "(":
                    if len(value_list) <= 1:
                        operator_list.pop()
                    else:
                        raise ValueError(
                            "Expression contains mismatched brackets.")
                if len(operator_list) <= 0:
                    if len(value_list) == 1:
                        root_node.set_left_child(value_list.pop())
                    else:
                        raise ValueError(
                            "Expression contains mismatched brackets.")
                actual_operator = operator_list.pop()
                sub_node = None
                while actual_operator != "(":
                    if actual_operator.is_monovalent():
                        if len(value_list) <= 0:
                            raise ValueError(
                                "A monovalent operator misses its argument.")
                        actual_value = value_list.pop()
                        sub_node = Node(actual_operator, actual_value)
                    else:
                        if len(value_list) <= 0:
                            raise ValueError(
                                "A bivalent operator misses its arguments.")
                        right_value = value_list.pop()
                        # peek at the operator to the left
                        if len(operator_list) <= 0:
                            raise ValueError(
                                "A bivalent operator misses its arguments.")
                        left_operator = operator_list[-1]
                        if self.operator_priority[left_operator] <= actual_operator:
                            if len(value_list) <= 0:
                                raise ValueError(
                                    "A bivalent operator misses its arguments.")
                            left_value = value_list.pop()
                            sub_node = self.Node(
                                actual_operator, left_value, right_value)
                        else:
                            sub_node = self.Node(actual_operator, left_value=None, right_value)

            else:
                raise ValueError("Token list contains unknown tokens.")

    class Operator:
        """
        Class representing a single mathematical operator.

        Connects the operator symbol with its corresponding function.
        """

        def __init__(self, operator_symbol, function):
            """
            Create an instance of Operator.

            operator_symbol:    a string representing the operator
            function:           the corresponding monovalent or bivalent
                                function
            """
            self.operator_symbol = operator_symbol
            self.function = function
            # evaluate the given function's number of arguments
            number_of_arguments = len(signature(function).parameters)
            if number_of_arguments == 1:
                self.is_monovalent = True
            elif number_of_arguments == 2:
                self.is_monovalent = False
            else:
                raise TypeError(
                    "Only monovalent or bivalent functions are allowed.")

        def __str__(self):
            """Return the operator symbol."""
            return self.operator_symbol

    class Value:
        """Class encapsulating a single object."""

        # TODO: this class should be abstract

        def __init__(self, value):
            """Create a new instance encapsulating the given object."""
            self.value = value

        def __str__(self):
            """Return a string representation of the encapsulated object."""
            return str(self.value)

    class Constant(Value):
        """Class representing a single constant."""

        def __init__(self, constant):
            """Create a new instance only if the input is a numeric type."""
            if isinstance(constant, Number):
                super().__init__(constant)
            else:
                raise TypeError(
                    "The Constant class only encapsulates numeric types.")

    class Variable(Value):
        """Class representing a single variable."""

        def __init__(self, variable_name):
            """Create a new instance only if the input is a string."""
            if isinstance(variable_name, str):
                super().__init__(variable_name)
            else:
                raise TypeError(
                    "The Variable class only encapsulates strings.")

    class Node:
        """Class representing a single node of the expression tree."""

        def __init__(self, operator=None, left_child=None, right_child=None):
            """
            Create a new node.

            operator:                   the specified Operator instance
            left_child, right_child:    either a Node instance, a Value subclass
                                        or None
            """
            self.operator = operator
            self.left_child = left_child
            self.right_child = right_child

        def __str__(self):
            if self.operator.is_monovalent:
                return str(self.operator) + "(" + str(self.left_child) + ")"
            else:
                return "(" + str(self.left_child) + str(self.operator) \
                    + str(self.right_child) + ")"

        def set_operator(self, operator):
            self.operator = operator

        def set_left_child(self, left_child):
            self.left_child = left_child

        def set_right_child(self, right_child):
            self.right_child = right_child

        def evaluate(self):
            if self.operator.is_monovalent:
                # operator is monovalent, therefore just check if the
                # corresponding data is a single value or a nested expression
                if isinstance(self.left_child, self.Value):
                    return self.operator.function(self.left_child.value)
                else:
                    return self.operator.function(self.left_child.evaluate())
            else:
                # operator is bivalent, therefore check which of
                # the two inputs is a single value and which one is a
                # nested expression
                if isinstance(self.left_child, self.Value):
                    # left child is a single value
                    if isinstance(self.right_child, self.Value):
                        return self.operator.function(
                            self.left_child.value, self.right_child.value
                        )
                    else:
                        return self.operator.function(
                            self.left_child.value, self.right_child.evaluate()
                        )
                else:
                    # left child is a nested expression
                    if isinstance(self.right_child, self.Value):
                        return self.operator.function(
                            self.left_child.evaluate(), self.right_child.value
                        )
                    else:
                        return self.operator.function(
                            self.left_child.evaluate(), self.right_child.evaluate()
                        )
