"""Module to represent mathematical expressions as a tree."""

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
            "-": 4
        }

        # create a list containing all operator symbols to simplify lookup
        self.operator_list = list(self.operator_priority.keys())

        # compute the length of the longest operator name
        self.longest_operator_length = 0
        for op in self.operator_list:
            if len(op) > self.longest_operator_length:
                self.longest_operator_length = len(op)

        # store the mathematical expression
        if mathematical_expression is None:
            self.mathematical_expression = ""
        else:
            self.mathematical_expression = self.delete_white_spaces(
                mathematical_expression)

        # store the length of the encapsulated expression
        self.mathematical_expression_length = len(self.mathematical_expression)

        # create the expression tree
        self.create_tree()

    def delete_white_spaces(self, expression):
        """Remove all white spaces within a given string."""
        expression_without_white_spaces = ""
        for character in expression:
            if not character.isspace():
                expression_without_white_spaces += character
        return expression_without_white_spaces

    def create_tree(self):
        """Create a tree out of the internal mathematical expression."""
        # list to store the expression's different tokens in order
        token_list = []
        # temporary list to construct constants or variables with
        # more than one character
        related_elements = []
        # move through the string character by character
        pointer = 0
        while (pointer < len(self.mathematical_expression)):
            character = self.mathematical_expression[pointer]
            if character.isalpha():
                # character is the first letter of a variable or an operator,
                # therefore check the following letters to decide which case
                # does apply
                related_elements.append(character)
                pointer += 1
                found_variable = False
                while (pointer < self.mathematical_expression_length):
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
                                token_list.append(actual_operator)
                                break
                    else:
                        # the actual subset of the expression has to be a
                        # variable
                        variable = "".join(related_elements)
                        variable_object = self.Variable(variable)
                        token_list.append(variable_object)
                        found_variable = True
                        break
                if not found_variable:
                    variable = "".join(related_elements)
                    variable_object = self.Variable(variable)
                    token_list.append(variable_object)
                del related_elements[:]
            elif character.isdigit():
                # Character is the first digit of an integer, therefore check
                # if it contains more than one digit.
                #
                # TODO: Maybe generalize this part to support floating
                # point numbers as well.
                related_elements.append(int(character))
                pointer += 1
                while (pointer < self.mathematical_expression_length):
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

                # create an object representing of the constant and insert
                # it into the list
                constant_object = self.Constant(constant)
                token_list.append(constant_object)
                del related_elements[:]
            else:
                # character is a special symbol such as / or * and therefore
                # clearly an operator
                token_list.append(character)
                pointer += 1
        print(token_list)

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
