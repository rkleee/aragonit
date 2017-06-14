"""Module to test the parser."""
import Expression

if __name__ == "__main__":
    expression_1 = Expression.Expression("(2 + sin(x)) * 5 - y ^ z")
    variables = {"x": 5, "y": 3, "z": 2}

    print(expression_1)
    print(expression_1.evaluate(variables))

    expression_2 = Expression.Expression(str(expression_1))

    print(expression_2)
    print(expression_2.evaluate(variables))
