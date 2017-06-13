from numbers import Number


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
