"""Module to handle different set operations."""

import itertools

import matplotlib.pyplot as plt


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

    def __add__(self, iteratable_data):
        """Use the + operator as a shortcut for the union function."""
        return union(self, iteratable_data)

    def __mul__(self, iteratable_data):
        """Use the * operator as a shortcut for the cartesian product."""
        return cartesianProduct(self, iteratable_data)

    def __sub__(self, iteratable_data):
        """Use the - operator as a shortcut for the complement function."""
        return complement(self, iteratable_data)

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
                y.append(item[1])
        return y

    def getCoordinates(self):
        """Return the data's x and y values as different lists."""
        x_values = []
        y_values = []
        for item in self.item_list:
            x_values.append(item[0])
            y_values.append(item[1])
        return x_values, y_values

    def plot(self):
        """Plot the encapsulated data."""
        x_values, y_values = self.getCoordinates()
        plt.plot(x_values, y_values, 'o')
        plt.show()


def union(iteratable_data_a, iteratable_data_b):
    """Return the union of iteratable data A and B as a set."""
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
            # both inputs are correct, therefore compute the union operation
            # as usual
            union_items = []
            # all items of dataset A have to be present in the union set
            for item in iteratable_data_a:
                union_items.append(item)
            # insert an element of B only if it is not already present
            for item in iteratable_data_b:
                if item not in iteratable_data_a:
                    union_items.append(item)
            union_set = Set(union_items)
            return union_set


def intersect(iteratable_data_a, iteratable_data_b):
    """Return the intersection of iteratable data A and B as a set."""
    # return immediately if input A or B is invalid
    if iteratable_data_a is None or len(iteratable_data_a) < 1:
        return Set([])
    if iteratable_data_b is None or len(iteratable_data_b) < 1:
        return Set([])
    # computation as usual because both inputs are valid
    intersect_items = []
    for item in iteratable_data_a:
        if item in iteratable_data_b:
            intersect_items.append(item)
    intersect_set = Set(intersect_items)
    return intersect_set


def complement(iteratable_data_a, iteratable_data_b=None):
    """Return the complement of iteratable data A and B as a set."""
    # return immediately if input A is invalid
    if iteratable_data_a is None or len(iteratable_data_a) < 1:
        return Set([])
    # validate input B and decide whether further processing is neccessary
    if iteratable_data_b is None or len(iteratable_data_b) < 1:
        return Set(iteratable_data_a)
    else:
        # both inputs are correct, therefore compute the complement as usual
        complement_items = []
        for item in iteratable_data_a:
            if item not in iteratable_data_b:
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
    """Create a set only with elements specified by given function."""
    specified_subset = []
    for item in iteratable_data:
        if isinstance(item, list):
            # item is a list, therefore use its first element as x value for
            # the selection function
            if selection_function(item[0], item[1]):
                specified_subset.append(item)
        else:
            # item is not a list and can be used directly for the
            # selection function
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
    """Compute binomial coefficients using power sets."""
    dummy_power_set = Set(range(n)).getPowerSet()
    number_of_subsets_with_length_k = 0
    for subset in dummy_power_set:
        if len(subset) == k:
            number_of_subsets_with_length_k += 1
    return number_of_subsets_with_length_k
