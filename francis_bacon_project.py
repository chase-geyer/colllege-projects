"""
The Kevin Bacon Game.

Replace "pass" with your code.
"""

import simpleplot
import comp140_module4 as movies

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """
        Initialize the queue.
        """
        self._queue = []
        
    def __len__(self):
        """
        Returns: an integer representing the number of items in the queue.
        """
        return len(self._queue)

    def __str__(self):
        """
        Returns: a string representation of the queue.
        """
        
        return str(self._queue)

    def push(self, item):
        """
        Add item to the queue.

        input:
            - item: any data type that's valid in a list
        """
        self._queue.append(item)

    def pop(self):
        """
        Remove the least recently added item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.

        Returns: the least recently added item.
        """
        return self._queue.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._queue = []


def bfs(graph, start_node):
    """
    Performs a breadth-first search on graph starting at the
    start_node.

    inputs:
        - graph: a graph object
        - start_node: a node in graph representing the start node

    Returns: a two-element tuple containing a dictionary
    associating each visited node with the order in which it
    was visited and a dictionary associating each visited node
    with its parent node.
    """
    current_queue = Queue()
    
    current_queue.push(start_node)
    
    visited = {start_node : 0}
    parents = {start_node: None}
    while len(current_queue) > 0:
        current = current_queue.pop()
        #print(graph.get_neighbors(current))
        if graph.get_neighbors != None:
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = visited[current] + 1
                    parents[neighbor] = current
                    current_queue.push(neighbor)
    for node in graph.nodes():
        if visited.get(node) == None:
            visited[node] = float('inf')
        if parents.get(node) == None:
            parents[node] = None
    #print(visited, parents)
    return (visited, parents)
#print(bfs(movies.load_test_graph('line'), 'C'))
#print(bfs(movies.load_test_graph('asymmetric2'), 'B'))
def distance_histogram(graph, node):
    """
    Computes the distance between the given node and all other
    nodes in that graph and creates a histogram of those distances.

    inputs:
        - graph: a graph object
        - node: a node in graph

    returns: a dictionary mapping each distance with the number of
    nodes that are that distance from node.
    """
    distance_dict = bfs(graph, node)[0]
    dist_hist = {}
    for key in distance_dict:
        distance = distance_dict[key]
        #print(distance)
        if dist_hist.get(distance) == None:
            dist_hist[distance_dict[key]] = 1
        else:
            dist_hist[distance_dict[key]] = dist_hist[distance_dict[key]] + 1
    return dist_hist
#print(distance_histogram(movies.load_test_graph('line'), 'A'))

def find_path(graph, start_person, end_person, parents):
    """
    Computes the path from start_person to end_person in the graph.

    inputs:
        - graph: a graph object with edges representing the connections between people
        - start_person: a node in graph representing the starting node
        - end_person: a node in graph representing the ending node
        - parents: a dictionary representing the parents in the graph

    returns a list of tuples of the path in the form:
        [(actor1, {movie1a, ...}), (actor2, {movie2a, ...}), ...]
    """
    #Figure out the shortest path by using parents dict to backtrace to the 
    #start node
    path_list = []
    current_node = end_person
    return_list = []
    if start_person == end_person:
        return_list = [(start_person, set())]
        
    while current_node != None:
        path_list.insert(0, current_node)
        current_node = parents.get(current_node)
    print(path_list)

    for idx in range(len(path_list)-1):
        attributes =  set(graph.get_attrs(path_list[idx], path_list[idx + 1]))
        return_list.append((path_list[idx], attributes))
        
    if len(path_list) > 1:
        return_list.append((path_list[-1], set()))
        
    return return_list

def play_kevin_bacon_game(graph, start_person, end_people):
    """
    Play the "Kevin Bacon Game" on the actors in the given
    graph.

    inputs:
        - graph: a a graph oject with edges representing the connections between people
        - start_person: a node in graph representing the node from which the search will start
        - end_people: a list of nodes in graph to which the search will be performed

    Prints the results out.
    """
    parents = bfs(graph, start_person)[1]
    return_list = []
    for person in end_people:
        return_list.append(find_path(graph, start_person, person, parents))
    return return_list

def run():
    """
    Load a graph and play the Kevin Bacon Game.
    """
    graph5000 = movies.load_graph('subgraph5000')

    if len(graph5000.nodes()) > 0:
        # You can/should use smaller graphs and other actors while
        # developing and testing your code.
        play_kevin_bacon_game(graph5000, 'Kevin Bacon',
            ['Amy Adams', 'Andrew Garfield', 'Anne Hathaway', 'Barack Obama', \
             'Benedict Cumberbatch', 'Chris Pine', 'Daniel Radcliffe', \
             'Jennifer Aniston', 'Joseph Gordon-Levitt', 'Morgan Freeman', \
             'Sandra Bullock', 'Tina Fey'])

        # Plot distance histograms
        for person in ['Kevin Bacon', 'Stephanie Fratus']:
            hist = distance_histogram(graph5000, person)
            simpleplot.plot_bars(person, 400, 300, 'Distance', \
                'Frequency', [hist], ["distance frequency"])

# Uncomment the call to run below when you have completed your code.

run()
