"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        # set of edges
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex does not exist in the graph")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if self.vertices[vertex_id]:
            return self.vertices[vertex_id]
        else:
            return None

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # if the node has not been visited print it and add its children to queue
        visited = set()
        node_queue = Queue()
        current = starting_vertex
        while current is not None:
            if current not in visited:
                if current is not None:
                    print(current)
                visited.add(current)
                for neighbor in self.vertices[current]:
                    node_queue.enqueue(neighbor)
            current = node_queue.dequeue()

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Same as dbt excpet with a stack instead of a queue
        visited = set()
        node_stack = Stack()
        current = starting_vertex
        while current is not None:
            if current not in visited:
                if current is not None:
                    print(current)
                visited.add(current)
                for neighbor in self.vertices[current]:
                    node_stack.push(neighbor)
            current = node_stack.pop()

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        # # I need to walk thr
        if visited == None:
            visited = set()
        if starting_vertex not in visited:
            print(starting_vertex)
            visited.add(starting_vertex)
            for vertex in self.vertices[starting_vertex]:
                self.dft_recursive(vertex, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty queue and enqueue A PATH TO the starting vertex ID
        node_queue = Queue()
        node_queue.enqueue([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while node_queue.size() > 0:
            # Dequeue the first PATH
            path_walked = node_queue.dequeue()
            # Grab the last vertex from the PATH
            last_vertex = path_walked[-1]
            # If that vertex has not been visited...
            if last_vertex not in visited:
                # CHECK IF IT'S THE TARGET
                if last_vertex == destination_vertex:
                    # IF SO, RETURN PATH
                    return path_walked
                # Mark it as visited...
                visited.add(last_vertex)
            # Then add A PATH TO its neighbors to the back of the queue
            for neighbor in self.get_neighbors(last_vertex):
                # COPY THE PATH
                path_copy = list(path_walked)
                # APPEND THE NEIGHBOR TO THE BACK
                path_copy.append(neighbor)
                node_queue.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create an empty stack and push A PATH TO the starting vertex ID
        node_stack = Stack()
        node_stack.push([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the stack is not empty...
        while node_stack.size() > 0:
            # Pop the first PATH
            path_walked = node_stack.pop()
            # Grab the last vertex from the PATH
            last_vertex = path_walked[-1]
            # If that vertex has not been visited...
            if last_vertex not in visited:
                # CHECK IF IT'S THE TARGET
                if last_vertex == destination_vertex:
                    # IF SO, RETURN PATH
                    return path_walked
                # Mark it as visited...
                visited.add(last_vertex)
            # Then add A PATH TO its neighbors to the back of the queue
            for neighbor in self.get_neighbors(last_vertex):
                # COPY THE PATH
                path_copy = path_walked.copy()
                # APPEND THE NEIGHBOR TO THE BACK
                path_copy.append(neighbor)
                node_stack.push(path_copy)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=set(), path_walked=[]):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # get a list of neighbors
        neighbors = self.get_neighbors(starting_vertex)

        # already visited nodes will return none
        # Else we return result of the recursive search
        if starting_vertex not in visited:
            visited.add(starting_vertex)
            path_copy = path_walked.copy()
            path_copy.append(starting_vertex)

            # We found it!
            if starting_vertex == destination_vertex:
                return path_copy

            # Lets keep looking
            for neighbor in neighbors:
                result = self.dfs_recursive(
                    neighbor, destination_vertex, visited, path_copy)
                if result is not None:
                    return result


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
