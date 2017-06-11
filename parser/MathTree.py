"""Module to represent mathematical expressions as a tree."""

from inspect import signature
from numbers import Number


class Expression:

    def __init__(self, mathematical_expression=None):
        """Initialize an expression."""
        if mathematical_expression is None:
            self.mathematical_expression = ""
        else:
            self.mathematical_expression = mathematical_expression


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
            raise TypeError("The Variable class only encapsulates strings.")


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
