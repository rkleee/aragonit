"""Module to handle different set operations."""

import itertools


class Set:
    """Class representing a set of different objects."""

    def __init__(self, iteratable_data=None):
        """Initialize a set with given data."""
        if iteratable_data is not None:
            self.item_list = self.eliminateDuplicates(iteratable_data)
        else:
            self.item_list = []
        self.initIterator()

    def initIterator(self):
        """
        Encapsulate the iterator initialization in a separate method.

        Is used to simplify inheritance.
        """
        self.actual_position_of_iterator = 0

    def __str__(self):
        """Return a string representation of all items within the set."""
        string_representation = "{"
        item_counter = 1
        for item in self.item_list:
            string_representation += str(item)
            if item_counter < len(self):
                string_representation += ", "
                item_counter += 1
        string_representation += "}"
        return string_representation

    def __iter__(self):
        """Return the instance object."""
        return self

    def __next__(self):
        """Return the next element in the set as long as it exists."""
        if self.actual_position_of_iterator < len(self):
            item = self.item_list[self.actual_position_of_iterator]
            self.actual_position_of_iterator += 1
            return item
        else:
            self.actual_position_of_iterator = 0
            raise StopIteration()

    def __contains__(self, element):
        """Return true if the specified item exists in the set."""
        for item in self.item_list:
            if item == element:
                return True
        return False

    def __len__(self):
        """Return the number of elements in the set."""
        return len(self.item_list)

    def __getitem__(self, index):
        """Access to item via index."""
        return self.item_list[index]

    def __mul__(self, iteratable_data):
        """Return the cartesian product of the actual set and the given set."""
        return cartesianProduct(self, iteratable_data)

    def getSpecifiedSubset(self, selection_function):
        """Create a subset according to given selection function."""
        return getSpecifiedSubset(self, selection_function)

    def getPowerSet(self):
        """Return a set containing all possible subsets."""
        power_set = []
        for i in range(len(self) + 1):
            # itertools.combinations(given_list, i) returns all subsets of
            # length i regarding the given list as a list of tuple instances
            subsets_of_length_i = itertools.combinations(self, i)
            # convert the list of tuples to a list of lists
            for subset_tuple in subsets_of_length_i:
                subset_tuple_as_list = []
                for num in subset_tuple:
                    subset_tuple_as_list.append(num)
                power_set.append(subset_tuple_as_list)
        return Set(power_set)

    def getAllItems(self):
        """Return a copy of the set's item list."""
        copied_item_list = []
        for item in self.item_list:
            copied_item_list.append(item)
        return copied_item_list

    def eliminateDuplicates(self, iteratable_data):
        """Take given data and create a list without duplicates."""
        items_without_duplicates = []
        for item in iteratable_data:
            if item not in items_without_duplicates:
                items_without_duplicates.append(item)
        return items_without_duplicates


class CartesianProduct(Set):
    """Class representing the cartesian product of two iteratable classes."""

    def __init__(
            self,
            iteratable_data_a=None,
            iteratable_data_b=None,
            selection_function=None):
        """Compute the cartesian product and create a corresponding set."""
        if selection_function is None:
            super().__init__(
                cartesianProduct(iteratable_data_a, iteratable_data_b)
            )
        else:
            specified_subset = getSpecifiedSubset(
                cartesianProduct(iteratable_data_a, iteratable_data_b),
                selection_function
            )
            super().__init__(specified_subset)

    def __call__(self, x):
        """
        Make the class callable.

        Return the y values of all inner tuples whose x values equal the input.
        """
        y = []
        for item in self.item_list:
            if item[0] == x:
                y.append(item)
        return y


def union(set_a, set_b):
    """Form the union of set A and set B."""
    union_items = set_a.getAllItems()
    for item in set_b:
        if item not in set_a:
            union_items.append(item)
    union_set = Set(union_items)
    return union_set


def intersect(set_a, set_b):
    """Make the intersection of set A and set B."""
    intersect_items = []
    for item in set_a:
        if item in set_b:
            intersect_items.append(item)
    intersect_set = Set(intersect_items)
    return intersect_set


def complement(set_a, set_b):
    """Form the complement of set A with set B."""
    complement_items = []
    for item in set_a:
        if item not in set_b:
            complement_items.append(item)
    complement_set = Set(complement_items)
    return complement_set


def cartesianProduct(iteratable_data_a, iteratable_data_b):
    """Return the cartesian product of two iteratable classes."""
    # check if one of the inputs is a None object or an empty list
    if iteratable_data_a is None or len(iteratable_data_a) < 1:
        if iteratable_data_b is None or len(iteratable_data_b) < 1:
            return Set([])
        else:
            return Set(iteratable_data_b)
    else:
        if iteratable_data_b is None or len(iteratable_data_b) < 1:
            return Set(iteratable_data_a)
        else:
            # both inputs are correct, therefore compute the cartesian product
            # as usual
            cartesian_product = []
            for item_a in iteratable_data_a:
                for item_b in iteratable_data_b:
                    cartesian_product.append([item_a, item_b])
            return Set(cartesian_product)


def getSpecifiedSubset(iteratable_data, selection_function):
    """Create a set containing elements specified by given function."""
    specified_subset = []
    for item in iteratable_data:
        if selection_function(item):
            specified_subset.append(item)
    return Set(specified_subset)


def vonNeumannOrdinalConstruction(n):
    """Use von Neumann's method to represent natural numbers."""
    if n == 0:
        return Set([])
    elif n == 1:
        return Set([[]])
    else:
        return union(
            Set(vonNeumannOrdinalConstruction(n - 1)),
            Set([vonNeumannOrdinalConstruction(n - 1)])
        )


def binomialCoefficient(n, k):
    """Compute binomial_coefficients using power sets."""
    dummy_set = Set(range(n))
    dummy_power_set = dummy_set.getPowerSet()
    number_of_subsets_with_length_k = 0
    for subset in dummy_power_set:
        if len(subset) == k:
            number_of_subsets_with_length_k += 1
    return number_of_subsets_with_length_k
