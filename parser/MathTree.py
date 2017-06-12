"""Module to represent mathematical expressions as a tree."""

from inspect import signature
from numbers import Number


class Expression:

    def __init__(self, mathematical_expression=None):
        """Create an expression tree out of given input."""
        # define all allowed operators and their corresponding priorities
        self.operator_priority = {
            "^": 1,
            "*": 2,
            "/": 2,
            "mod": 3,
            "+": 4,
            "-": 4
        }
        self.operator_list = list(self.operator_priority.keys())

        # compute the number of letters of the longest operator name
        self.length_of_longest_operator = 0
        for op in self.operator_list:
            if len(op) > self.length_of_longest_operator:
                self.length_of_longest_operator = len(op)

        # create the expression tree
        if mathematical_expression is None:
            self.mathematical_expression = ""
            self.root_node = None
        else:
            self.mathematical_expression = self.delete_white_spaces(
                mathematical_expression)
            self.root_node = None
        self.create_tree()

    def delete_white_spaces(self, mathematical_expression):
        """Remove all white spaces within a given string."""
        expression_without_white_spaces = ""
        for character in mathematical_expression:
            if not character.isspace():
                expression_without_white_spaces += character
        return expression_without_white_spaces

    def create_tree(self):
        """Create a tree out of the internal mathematical expression."""
        stack = []

        # temporary list to construct constants or variables with more than
        # one character
        temporary_list = []

        # move through the string character by character
        pointer = 0
        while (pointer < len(self.mathematical_expression)):
            character = self.mathematical_expression[pointer]
            if character.isalpha():
                # Character is a letter.
                # ======================
                # Temporarily store this character in a list and add the
                # following letters one by one to check if it
                # form a valid operator.
                temporary_list.append(character)
                temporary_pointer = pointer + 1
                temporary_length = 2
                found_operator = False
                while (
                    temporary_pointer < len(self.mathematical_expression)
                    and temporary_length <= self.length_of_longest_operator
                ):
                    temporary_character = self.mathematical_expression[
                        temporary_pointer
                    ]
                    if temporary_character.isalpha():
                        temporary_list.append(temporary_character)
                        actual_operator = "".join(temporary_list)
                        if actual_operator in self.operator_list:
                            stack.append(actual_operator)
                            found_operator = True
                            break
                        temporary_pointer += 1
                        temporary_length += 1
                    else:
                        
                if found_operator:
                    pointer = temporary_pointer + 1
                else:

                    variable_object = self.Variable(character)
                    stack.append(variable_object)
                del temporary_list[:]
            elif character.isdigit():
                # Character is a number.
                # =====================
                # The number may contain more than one digit.
                while (
                    pointer < len(self.mathematical_expression)
                    and self.mathematical_expression[pointer].isdigit()
                ):
                    temporary_list.append(
                        int(self.mathematical_expression[pointer])
                    )
                    pointer += 1
                # construct an integer out of the stored digits
                length = len(temporary_list)
                constant = 0
                for i in temporary_list:
                    constant += i * (10 ** (length - 1))
                    length -= 1
                # push the constant onto the stack
                constant_object = self.Constant(constant)
                stack.append(constant_object)
                del temporary_list[:]
            else:
                # character is a special symbol such as / or *
                if character == "(":
                    stack.append(character)
                elif character == ")":
                    break

    class Operator:
        """
        Class representing a single mathematical operator.

        Connects the operator symbol with its corresponding function.
        """

        def __init__(self, operator_symbol, function):
            """
            Create an instance of Operator.

            operator_symbol:    a string representing the operator
            function:           the corresponding monovalent or bivalent function
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

        def __init__(self, operator, left_child, right_child=None):
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

        def evaluate(self):
            if self.operator.is_monovalent:
                # operator is monovalent, therefore just check if the
                # corresponding data is a single value or a nested expression
                if isinstance(self.left_child, Value):
                    return self.operator.function(self.left_child.value)
                else:
                    return self.operator.function(self.left_child.evaluate())
            else:
                # operator is bivalent, therefore check which of
                # the two inputs is a single value and which one is a
                # nested expression
                if isinstance(self.left_child, Value):
                    # left child is a single value
                    if isinstance(self.right_child, Value):
                        return self.operator.function(
                            self.left_child.value, self.right_child.value
                        )
                    else:
                        return self.operator.function(
                            self.left_child.value, self.right_child.evaluate()
                        )
                else:
                    # left child is a nested expression
                    if isinstance(self.right_child, Value):
                        return self.operator.function(
                            self.left_child.evaluate(), self.right_child.value
                        )
                    else:
                        return self.operator.function(
                            self.left_child.evaluate(), self.right_child.evaluate()
                        )


def plus(x, y):
    """Plus function."""
    return x + y


def minus(x, y):
    """Minus function."""
    return x - y


def mult(x, y):
    """Multiplication function."""
    return x * y


def div(x, y):
    """Division function."""
    return x / y


def mod(x, y):
    """Modulo function."""
    return x % y


def pow(x, y):
    """Power function."""
    return x ** y
