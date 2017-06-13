from inspect import signature


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
