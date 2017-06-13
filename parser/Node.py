import Value


class Node:
    """Class representing a single node of the expression tree."""

    def __init__(self, operator, left_child, right_child=None):
        """
        Create a new node.
        operator:                   the specified Operator instance
        left_child, right_child:    either a Node, a subclass of Value
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
            if isinstance(self.left_child, Value.Value):
                return self.operator.function(self.left_child.value)
            else:
                return self.operator.function(self.left_child.evaluate())
        else:
            # operator is bivalent, therefore check which of
            # the two inputs is a single value and which one is a
            # nested expression
            if isinstance(self.left_child, Value.Value):
                # left child is a single value
                if isinstance(self.right_child, Value.Value):
                    return self.operator.function(
                        self.left_child.value, self.right_child.value
                    )
                else:
                    return self.operator.function(
                        self.left_child.value, self.right_child.evaluate()
                    )
            else:
                # left child is a nested expression
                if isinstance(self.right_child, Value.Value):
                    return self.operator.function(
                        self.left_child.evaluate(), self.right_child.value
                    )
                else:
                    return self.operator.function(
                        self.left_child.evaluate(), self.right_child.evaluate()
                    )
