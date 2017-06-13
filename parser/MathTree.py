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

        # store the mathematical expression
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
        # move through the string character by character
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
                del related_elements[:]
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

                # create an object representing of the constant and insert
                # it into the list
                constant_object = self.Constant(constant)
                token_list.append(constant_object)
                del related_elements[:]
            else:
                # character is a special symbol such as / or * and therefore
                # clearly an operator
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
        return token_list

    def create_operator(self, operator_symbol):
        """Match the given operator symbol to its corresponding function."""
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
        helper_list = []

        # move forwards through the token list
        for token in self.token_list:
            if token != ")":
                helper_list.append(token)
            else:
                # move backwards through the helper list
                pointer = len(helper_list) - 1
                if isinstance(helper_list[pointer], self.Operator):
                    raise ValueError("One operator has a missing argument.")
                while helper_list[pointer] != "(":
                    if isinstance(helper_list[pointer], self.Variable) \
                            or isinstance(helper_list[pointer], self.Constant):

                helper_list.pop()



                while last_operator != "(":
                    if last_operator.is_monovalent():
                        last_value = value_stack.pop()
                        node = self.Node(last_operator, last_value)
                    else:


            if token == ")":
                last_item = stack.pop()
                while last_item != "(":
                    if isinstance(last_item, self.Constant):
                        return None

            else:
                stack.append(token)

                oken einlesen.

    WENN Token IST - Argumenttrennzeichen:
        BIS Stack - Spitze IST öffnende - Klammer:
            Stack - Spitze ZU Ausgabe.
            FEHLER - BEI Stack IST - LEER:
                GRUND(1) Ein falsch platziertes Argumenttrennzeichen.
                GRUND(2) Der schließenden Klammer geht keine öffnende voraus.
            ENDEFEHLER
        ENDEBIS
    ENDEWENN
    WENN Token IST - Operator
        SOLANGE Stack IST - NICHT - LEER UND Stack - Spitze IST Operator UND
        Token IST - linksassoziativ UND Präzedenz von Token IST - KLEINER Präzedenz von Stack - Spitze
            Stack - Spitze ZU Ausgabe.
        ENDESOLANGE
        Token ZU Stack.
    ENDEWENN
    WENN Token IST öffnende - Klammer:
        Token ZU Stack.
    ENDEWENN
    WENN Token IST schließende - Klammer:
        BIS Stack - Spitze IST öffnende - Klammer:
            FEHLER - BEI Stack IST - LEER:
                GRUND(1) Der schließenden Klammer geht keine öffnende voraus.
            ENDEFEHLER
            Stack - Spitze ZU Ausgabe.
        ENDEBIS
        Stack - Spitze(öffnende - Klammer) entfernen
        WENN Stack - Spitze IST - Funktion:
            Stack - Spitze ZU Ausgabe.
        ENDEWENN
    ENDEWENN


ENDESOLANGE
BIS Stack IST - LEER:

    FEHLER - BEI Stack - Spitze IST öffnende - Klammer:
        GRUND(1) Es gibt mehr öffnende als schließende Klammern.
    ENDEFEHLER
    Stack - Spitze ZU Ausgabe.

ENDEBIS

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
