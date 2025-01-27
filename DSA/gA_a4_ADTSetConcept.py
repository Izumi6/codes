'''
To create ADT that implement the "set" concept.
a. Add (newElement) -Place a value into the set
b. Remove (element) Remove the value
c. Contains (element) Return true if element is in collection
d. Size () Return number of values in collection Iterator () 
   Return an iterator used to loop over collection
e. Intersection of two sets
f. Union of two sets
g. Difference between two sets
h. Subset
'''

class Set:
    def __init__(self):
        self.elements = []

    def add(self, newElement):
        if newElement not in self.elements:
            self.elements.append(newElement)

    def remove(self, element):
        if element in self.elements:
            self.elements.remove(element)

    def contains(self, element):
        return element in self.elements

    def size(self):
        return len(self.elements)

    def iterator(self):
        return iter(self.elements)

    def intersection(self, otherSet):
        intersectionSet = Set()
        for element in self.elements:
            if otherSet.contains(element):
                intersectionSet.add(element)
        return intersectionSet

    def union(self, otherSet):
        unionSet = Set()
        unionSet.elements = self.elements.copy()
        for element in otherSet.elements:
            unionSet.add(element)
        return unionSet

    def difference(self, otherSet):
        differenceSet = Set()
        for element in self.elements:
            if not otherSet.contains(element):
                differenceSet.add(element)
        return differenceSet

    def subset(self, otherSet):
        for element in self.elements:
            if not otherSet.contains(element):
                return "Set 1 is Not a Subset of Set 2"
        return "Set 1 is a Subset of Set 2"

    def display(self):
        print("Current Set:", self.elements)


# Example usage
set1 = Set()
set1.add(1)
set1.add(2)
set1.add(3)

set2 = Set()
set2.add(3)
set2.add(4)
set2.add(5)

print("Set 1:", list(set1.iterator()))
print("Set 2:", list(set2.iterator()))
print("Intersection:", list(set1.intersection(set2).iterator()))
print("Union:", list(set1.union(set2).iterator()))
print("Difference (Set 1 - Set 2):", list(set1.difference(set2).iterator()))
print(set1.subset(set2))
