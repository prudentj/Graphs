
# ancestors will contain an array of tuples with index 0 being the parent and 1 the child
# test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

# Write a function that, given the dataset and the ID of an individual in the dataset,
#  returns their earliest known ancestor –
#  the one at the farthest distance from the input individual.
#  If there is more than one ancestor tied for "earliest",
#  return the one with the lowest numeric ID.
#  If the input individual has no parents, the function should return -1.


def earliest_ancestor(ancestors, starting_node):
    # Construct a table of relationships
    # key is child, value is array contains parrents
    geneology = {}
    for birth in ancestors:
        parent = birth[0]
        child = birth[1]
        if child not in geneology:
            geneology[child] = [parent]
        else:
            geneology[child].append(parent)

    # Have a variable with the current shortest paths to iterate through and one
    # if this child is an orphan return negative 1
    if starting_node not in geneology:
        return -1
    children = set([starting_node])
    parents = set()

    # Will be true when we reach the end of the line
    furthest_gen = False
    # find the node containing the child
    while not furthest_gen:
        for child in children:
            if child in geneology:
                for parent in geneology[child]:
                    parents.add(parent)
        # Checking to see if set is empty
        if not parents:
            furthest_gen = True
            break
        # Now going to set parents as children and reseting parrents
        children = parents
        parents = set()
    # finding the smallest child and returning it
    return min(children)


if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                      (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    earliest_ancestor(test_ancestors, 1)
