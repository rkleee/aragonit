"""Main module to test the CustomSet classes."""
import CustomSet as cs

if __name__ == "__main__":
    list1 = ["a", "b", "c", "d"]
    list2 = [1, 2, 3]
    set1 = cs.Set(list1)
    set2 = cs.Set(list2)

    subset = set2.getSpecifiedSubset(lambda x: x < 2)
    print(subset)

    cp = cs.CartesianProduct(list1, list2, lambda l: l[0] == "a")
    print(cp)
    print(cp("a"))
