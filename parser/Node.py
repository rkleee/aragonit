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

    def evaluate(self, variables=None):
        if self.operator.is_monovalent:
            # operator is monovalent, therefore just check if the
            # corresponding data is a constant, a variable or a
            # nested expression
            if isinstance(self.left_child, Value.Constant):
                # left child is a constant
                return self.operator.function(self.left_child.value)
            elif isinstance(self.left_child, Value.Variable):
                # left child is a variable
                return self.operator.function(variables[str(self.left_child)])
            else:
                # left child is a nested expression
                return self.operator.function(
                    self.left_child.evaluate(variables)
                )
        else:
            # operator is bivalent, therefore check which of
            # the two inputs are constants, variables or
            # nested expressions
            if isinstance(self.left_child, Value.Constant):
                if isinstance(self.right_child, Value.Constant):
                    # left and right children are constants
                    return self.operator.function(
                        self.left_child.value,
                        self.right_child.value
                    )
                elif isinstance(self.right_child, Value.Variable):
                    # left child is a constant, right child a variable
                    return self.operator.function(
                        self.left_child.value,
                        variables[str(self.right_child)]
                    )
                else:
                    # left child is a constant, right child a nested expression
                    return self.operator.function(
                        self.left_child.value,
                        self.right_child.evaluate(variables)
                    )
            elif isinstance(self.left_child, Value.Variable):
                if isinstance(self.right_child, Value.Constant):
                    # left child is a variable, right child a constant
                    return self.operator.function(
                        variables[str(self.left_child)],
                        self.right_child.value
                    )
                elif isinstance(self.right_child, Value.Variable):
                    # left and right children are variables
                    return self.operator.function(
                        variables[str(self.left_child)],
                        variables[str(self.right_child)]
                    )
                else:
                    # left child is a variable, right child a nested expression
                    return self.operator.function(
                        variables[str(self.left_child)],
                        self.right_child.evaluate(variables)
                    )
            else:
                if isinstance(self.right_child, Value.Constant):
                    # left child is a nested expression, right child a constant
                    return self.operator.function(
                        self.left_child.evaluate(variables),
                        self.right_child.value
                    )
                elif isinstance(self.right_child, Value.Variable):
                    # left child is a nested expression, right child a variable
                    return self.operator.function(
                        self.left_child.evaluate(variables),
                        variables[str(self.right_child)]
                    )
                else:
                    # left and right children are nested expressions
                    return self.operator.function(
                        self.left_child.evaluate(variables),
                        self.right_child.evaluate(variables)
                    )
