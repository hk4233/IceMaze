"""
CSCI-603: Graphs
Author: Sean Strout @ RIT CS

This is the lecture problem for determining paths between stations in a
subway system.
"""

from graph import Graph
from searchAlgos import canReachDFS, findPathDFS, findShortestPath

class Subway:
    """
    The complete subway system is represented in this class, as a matrix
    of station to station connections.
    :slot: matrix (Graph): The matrix of stations
    :slot: stationNames (dict): A mapping of station id (int) to
        station name (str)
    :slot: stationIDs (dict): A mapping of station name (string) to
        station id (int)
    """
    __slots__ = 'graph', 'stationNames', 'stationIDs'

    def __init__(self, filename):
        """
        Construct the subway system
        :param filename (str): The input file (see boston.txt or lecture.txt)
        :return: None
        """

        # initialize structures
        self.stationNames = {}
        self.stationIDs = {}
        self.graph = Graph()
        with open(filename) as f:
            for line in f:
                if len(line) > 0 and line[0] != '#':
                    # e.g. "20 NorthStation   Green 19 22  Orange 15 22"
                    fields = line.split()
                    id = int(fields[0])
                    self.stationNames[id] = fields[1]
                    self.stationIDs[fields[1]] = id
                    # iterate over the lines, 3 items at a time, e.g.:
                    #   "Green 19 22"
                    for color, outbound, inbound in zip(*[iter(fields[2:])]*3):
                        # undirected edges, so connect inbound to outbound and
                        # vice versa
                        if int(outbound) > 0:
                            self.graph.addEdge(id, int(outbound))
                        if int(inbound) > 0:
                            self.graph.addEdge(id, int(inbound))

    def __str__(self):
        """
        Return a string representation of the matrix's adjacency list, e.g.:
            Node0: ['Node1', 'Node2']
            Node1: ['Node0']
            ...
        :return: The string for the matrix
        """
        result = ''
        for station in self.graph:
            result += self.stationNames[station.id] + ': '
            result += str([self.stationNames[neighbor.id] \
                           for neighbor in station.getConnections()])
            result += '\n'
        return result

    def printPath(self, start, end, path):
        """
        Display a path from start_block to end_block in the form:
            Can travel from {start_block} to {end_block} by # stations:
                A to B
                B to C
                ...
        :param start_block (str): Start station name
        :param end_block (str): End station name
        :param path (list): A list of strings representing the path from
            start_block to end_block
        :return: None
        """
        print('Can travel from', start, 'to', end, 'by', len(path), 'stations:')
        for i in range(len(path)-1):
            print('\t' + self.stationNames[path[i].id], 'to', self.stationNames[path[i+1].id])

    def mainLoop(self):
        """
        The main loop runs here.
        :return: None
        """
        while (True):
            print('1. Display matrix')
            print('2. Can reach')
            print('3. Find any path')
            print('4. Find shortest path')
            option = input('subway> ')
            if option == "":
                break
            option = int(option)
            if option == 1:
                print(self)
                continue

            # loop until we get a valid start_block and end_block station
            while True:
                start = input('Enter start_block station name: ')
                if start not in self.stationIDs:
                    print(start, 'not found in matrix')
                    continue
                end = input('Enter end_block station name: ')
                if end not in self.stationIDs:
                    print(end, 'not found in matrix')
                    continue
                break

            # get the vertices
            startVertex = self.graph.getVertex(self.stationIDs[start])
            endVertex = self.graph.getVertex(self.stationIDs[end])

            # perform the search and display the results
            if option == 2:
                reachable = canReachDFS(startVertex, endVertex)
                if reachable:
                    print('There is a path between', start, 'and', end)
                else:
                    print('There is no path between', start, 'and', end)
            elif option == 3:
                path = findPathDFS(startVertex, endVertex)
                if path != None:
                    self.printPath(start, end, path)
                else:
                    print('There is no path between', start, 'and', end)
            else:
                path = findShortestPath(startVertex, endVertex)
                if path != None:
                    self.printPath(start, end, path)
                else:
                    print('There is no path between', start, 'and', end)
            print()

def main():
    """
    The main function prompts for the file name and enters the
    main loop.
    :return: None
    """
    try:
        subway = Subway(input('Enter filename: '))
        subway.mainLoop()
    except IOError as err:  # if error with file name
        print(err)

if __name__ == '__main__':
    main()