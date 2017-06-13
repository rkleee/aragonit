"""Module to test the parser."""
import MathTree as mt

if __name__ == "__main__":
    # plus = mt.Operator("+", lambda x, y: x + y)
    # minus = mt.Operator("-", lambda x, y: x - y)
    # mult = mt.Operator("*", lambda x, y: x * y)
    # sin = mt.Operator("sin", lambda x: math.sin(x))
    #
    # nodePlus = mt.Node(plus, mt.Constant(3), mt.Constant(4))
    # nodeMinus = mt.Node(minus, mt.Constant(4), mt.Constant(1))
    #
    # nodeMult = mt.Node(mult, mt.Constant(2), nodePlus)
    #
    # print(nodeMult)
    # print(nodeMult.evaluate())

    e = mt.Expression("sin(abc) + (5 * abc)")
