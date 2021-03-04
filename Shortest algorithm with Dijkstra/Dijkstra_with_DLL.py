# Created by Joao Jesus, Aniket Basu and Lukas Tatarunas
from collections import defaultdict
import csv


# from gui import results


class Node:
    """Node class for doubly linked list"""
    def __init__(self, data):
        self.data = data;
        self.previous = None;
        self.next = None;


class DoublyLinkedList:
    """Represent the head and end of the doubly linked list"""

    def __init__(self):
        self.head = None;
        self.end = None;
        self.length = 0
        # addNode() will add a node to the list

    def addNode(self, data):
        """Create a new node"""
        newNode = Node(data);
        self.length += 1
        # If list is empty, create a head node
        if self.head == None:
            # Both head and end will point to newNode
            self.head = self.end = newNode;
            # head's previous will point to None
            self.head.previous = None;
            # end's next will point to None, as it is the last node of the list
            self.end.next = None;
        else:
            # newNode will be added after end such that end's next will point to newNode
            self.end.next = newNode;
            # newNode's previous will point to end
            newNode.previous = self.end;
            # newNode will become new end
            self.end = newNode;
            # As it is last node, end's next will point to None
            self.end.next = None;

    def length_list(self):
        return self.length

    def display(self):
        # Node current will point to head
        current = self.head;
        if (self.head == None):
            print("List is empty");
            return;
        print("Nodes of doubly linked list: ");
        while (current != None):
            # Prints each node by incrementing pointer.
            print(current.data),;
            current = current.next;

    def traverse_list(self, index) -> list:
        """Function to traverse through the Double Linked List using a pointer"""
        current = self.head
        if self.head is None:  # check if the list is empty
            print("List is empty")
        elif index < 0 or index > self.length:  # check if number entered is valid to search the list
            print("Invalid range")
        elif index == 0:  # if 0 is entered, return the head element
            return self.head.data
        elif index > 0 and index < self.length:  # find elements in between head and end elements
            for i in range(index):
                current = current.next;
            return current.data
        elif index == self.length:  # if number entered matches length, return end element
            return self.end.data

    def find_node(self, line=None, stn=None) -> list:
        """Function to find node that contains certain elements"""
        output = DoublyLinkedList()
        for i in range(self.length):
            temp = self.traverse_list(i)
            if temp.get('ï»¿Line') == line or temp.get('Station1') == stn or temp.get('Station2') == stn:
                output.addNode(temp)
        return output

    def find_nodes_by_station_pair(self, stn1, stn2) -> str:
        """Function to find node line based on a pair of elements provided"""
        output = None
        for i in range(self.length):
            temp = self.traverse_list(i)
            if temp.get('Station1') == stn1 and temp.get('Station2') == stn2 or temp.get(
                    'Station1') == stn2 and temp.get('Station2') == stn1:
                output = ((temp.get('ï»¿Line')))
        return output

    def find_nodes_by_station_pair_time(self, stn1, stn2) -> int:
        """Function to find node time based on a pair of elements provided"""
        time = None
        for i in range(self.length):
            temp = self.traverse_list(i)
            if temp.get('Station1') == stn1 and temp.get('Station2') == stn2 or temp.get(
                    'Station1') == stn2 and temp.get('Station2') == stn1:
                time = ((temp.get('time')))
        return time


class Graph():
    def __init__(self):
        """
        self.edges is a dict of every possible next nodes
        e.g. {'Z': ['A', 'B', 'C',], ...}
        self.weights contains the weights between two nodes,
        ...the two nodes serving as the tuple
        e.g. {('Z', 'A'): 11, ('Z', 'C'): 2.4, ...}
        self.lines contains the Line_Id(Line Name) between two nodes,
        ...the two nodes serving as the tuple
        e.g. {('Z', 'A'): Bakerloo, ('Z', 'C'): District, ...}
        """
        self.lines = {}
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, line_iD, from_node, to_node, weight):
        """Function to connect the different stations, weight, and line_Id both ways"""
        # catering for the type of line in source and destination nodes
        self.lines[(from_node, to_node)] = line_iD
        self.lines[(to_node, from_node)] = line_iD
        # connecting nodes from both sides
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        # catering for the source and destination nodes
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight
        # combining the indegree and outdegree weights were possible


def builder(time, input_file=None):
    """Creates the doubly linked list and the graph using the time input"""
    train_data = DoublyLinkedList()
    graph = Graph()
    edges = []
    if 900 <= time <= 1600 or 1900 <= time <= 2359:  # Check the time and load correct data
        input_file = csv.DictReader(open("Underground Data Bakerloo.csv"))
        for x in input_file:
            train_data.addNode(x)
    else:
        input_file = csv.DictReader(open("Underground Data Tweaked.csv"))
        for x in input_file:
            train_data.addNode(x)

    for i in range(0, train_data.length):  # Create the graph utilizing the doubly linked list object
        temp_data = train_data.traverse_list(i)
        # line = temp_data.get('\ufeffLine')
        line = temp_data.get('ï»¿Line')
        stn1 = temp_data.get('Station1')
        stn2 = temp_data.get('Station2')
        time_station = float(temp_data.get('time'))
        edges_sublist = (line, stn1, stn2, time_station)
        edges.append(edges_sublist)
        for edge in edges:
            graph.add_edge(*edge)
    return graph


class Dijkstra():
    def __init__(self, initial, end):
        self._initial = initial
        self._end = end
        self._shortest_paths = {self._initial: (None, 0)}
        self._current_node = self._initial
        self._visited = set()

    def find_path(self, graph):
        """Function that implements Dijkstra algorithm to find the fastest path/path with the lowest weight"""
        while self._current_node != self._end:
            self._visited.add(self._current_node)
            destinations = graph.edges[self._current_node]
            weight_to_current_node = self._shortest_paths[self._current_node][1]
            for next_node in destinations:
                weight = graph.weights[(self._current_node, next_node)] + weight_to_current_node
                if next_node not in self._shortest_paths:
                    self._shortest_paths[next_node] = (self._current_node, weight)
                else:
                    current_shortest_weight = self._shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        self._shortest_paths[next_node] = (self._current_node, weight)

            next_destinations = {node: self._shortest_paths[node] for node in self._shortest_paths if
                                 node not in self._visited}
            if not next_destinations:
                return "Route Not Possible"
            # the next node is the destination with the lowest weight
            self._current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # determining the shortest path
        self.path = []
        while self._current_node is not None:
            self.path.append(self._current_node)
            next_node = self._shortest_paths[self._current_node][0]
            self._current_node = next_node
        # Reverses the  path
        self.path = self.path[::-1]
        self.time = weight + len(self.path)
        return self.path, self.time


def find_lines(path_list, time_of_travel, start_station=None, end_station=None):
    """Function to the find the Line_Id corresponding with the Stations returned by the find_path function"""
    output = []
    time = []
    train_data = DoublyLinkedList()
    if 900 <= time_of_travel <= 1600 or 1900 <= time_of_travel <= 2400:  # Load file according to the time entered
        data = csv.DictReader(open("Underground Data Bakerloo.csv"))
    else:
        data = csv.DictReader(open("Underground Data Tweaked.csv"))
    for x in data:  # Create doubly linked list with selected data
        train_data.addNode(x)
    for station in path_list:  # Utilize search functions from the doubly linked list class to find the line
        if path_list.index(station) == len(path_list) - 1:
            station = path_list[-1]
            station2 = path_list[path_list.index(station) - 1]
            output.append(train_data.find_nodes_by_station_pair(station, station2))
            time.append(train_data.find_nodes_by_station_pair_time(station, station2))

        else:
            station2 = path_list[path_list.index(station) + 1]
            output.append(train_data.find_nodes_by_station_pair(station, station2))
            time.append(train_data.find_nodes_by_station_pair_time(station, station2))

    return output, time
