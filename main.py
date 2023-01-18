"""
file: main.py
Description: An implementation of a Get of the ICE maze

Language: python3

@author: Anurag Kacham (ak4579)
@author: Hima Bindu Krovvidi (hk4233)
"""

import sys
from graph import Graph

# This is a global variable.
STONE = '*'


def findNeighbors(row, col, matrix):
    """
    This method is used to find the neighbors in all directions
    for all the vertices in the matrix.

    :param row: int
    :param col: int
    :param matrix: provided matrix
    :return: tuple, which consists of the vertices
    """
    top, bottom, left, right = None, None, None, None
    # neighbors will be added based on the conditions being evaluated,
    # which are include everything till that point
    # if it's a stone, else keep adding everything until it reaches end_block.
    curr_iter = col - 1
    while curr_iter >= 0:
        if matrix[row][curr_iter] == STONE and curr_iter + 1 != col:
            left = (row, curr_iter + 1)
            break
        if curr_iter == 0:
            left = (row, curr_iter)
            break
        curr_iter -= 1
    curr_iter = col + 1
    while len(matrix[0]) > curr_iter:
        if curr_iter == len(matrix[0]) - 1:
            right = (row, curr_iter)
            break
        if matrix[row][curr_iter] == STONE and curr_iter - 1 != col:
            right = (row, curr_iter - 1)
            break
        curr_iter += 1
    curr_iter = row - 1
    while curr_iter >= 0:
        if matrix[curr_iter][col] == STONE and curr_iter + 1 != row:
            top = (curr_iter + 1, col)
            break
        if curr_iter == 0:
            top = (curr_iter, col)
            break
        curr_iter -= 1
    curr_iter = row + 1
    while curr_iter < len(matrix):
        if matrix[curr_iter][col] == STONE and curr_iter - 1 != row:
            bottom = (curr_iter - 1, col)
            break
        if curr_iter == len(matrix) - 1:
            bottom = (curr_iter, col)
            break
        curr_iter += 1
    return left, right, top, bottom


def shortest_path_map(escape_block, matrix):
    """
    This method is used to calculate the shortest path from
    the current vertex to the escape vertex.
    :param escape_block: escape vertex
    :param matrix: provided matrix
    :return:
    """
    # a dictionary will be maintained, for constructing shortest path from
    # current vertices to end vertex or to update
    temp_map = {}
    for vertex in matrix.getVertices():
        # if the current vertex matches the escape_block,
        # go on to the next vertex.
        if vertex == escape_block:
            continue
        total_edges = 0
        # shortest path, if possible, will be found from current vertex.
        temp_shortest_path = shortest_path(matrix.getVertex(vertex),
                                           matrix.getVertex(escape_block))
        temp_vertex = (vertex[1], vertex[0])
        if temp_shortest_path is not None:
            total_edges = len(temp_shortest_path) - 1
        if temp_map.get(total_edges) is None:
            temp_map[total_edges] = [temp_vertex]
        else:
            temp_map[total_edges].append(temp_vertex)
    return temp_map


def shortest_path(start_block, end_block):
    """
    This method will be used to calculate the shortest path between the
    given vertex and end vertex, if one exists.
    :param start_block: starting vertex in the matrix
    :param end_block: destination vertex in the matrix
    :return:
    """
    list_for_path = [start_block]
    temp_before = {start_block: None}
    while len(list_for_path) > 0:
        ele = list_for_path.pop(0)
        if ele == end_block:
            break
        for neighbor in ele.getConnections():
            if neighbor not in temp_before:
                temp_before[neighbor] = ele
                list_for_path.append(neighbor)
    if end_block in temp_before:
        temp_list_for_path = []
        ele = end_block
        while ele != start_block:
            temp_list_for_path.insert(0, ele)
            ele = temp_before[ele]
        temp_list_for_path.insert(0, start_block)
        return temp_list_for_path
    else:
        return None


def construct_graph(matrix, exit_block):
    """
    Takes the input file and constructs a graph.
    :param matrix: matrix
    :param exit_block: exit block in the matrix
    :return:
    """
    temp_graph = Graph()
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == '.':
                if temp_graph.getVertex((row, col)) is None:
                    temp_graph.addVertex((row, col))
                left, right, top, bottom = \
                    findNeighbors(row, col, matrix)

                if left:
                    temp_graph.addEdge((row, col), left)

                if right is None and (row, col) == exit_block:
                    right = (exit_block[0], exit_block[1] + 1)
                    temp_graph.addEdge((row, col), right)
                elif right == exit_block:
                    right = (exit_block[0], exit_block[1] + 1)
                    temp_graph.addEdge((row, col), right)
                else:
                    temp_graph.addEdge((row, col), right)

                if top:
                    temp_graph.addEdge((row, col), top)

                if bottom:
                    temp_graph.addEdge((row, col), bottom)

            else:
                if temp_graph.getVertex((row, col)) is None:
                    temp_graph.addVertex((row, col))
    return temp_graph


def parse_args(file_name):
    """
    Reads the file and returns matrix of the pond.
    :param file_name: file name as string
    :return:
    """
    with open(file_name) as file:
        argument = file.readline().strip()
        ls = []
        for line in file:
            line = line.strip().split()
            ls.append(line)
    return ls, argument


def main():
    """
    Main function.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 pond.py <file_name>")
        sys.exit(1)
    pond, argument = parse_args(sys.argv[1])
    escape_row = int(argument.split()[2])
    escape_block = (escape_row, len(pond[0]))
    exit_block = (escape_row, len(pond[0]) - 1)
    graph = construct_graph(pond, exit_block)
    temp_map = shortest_path_map(escape_block, graph)
    for key in sorted(temp_map.keys()):
        if key != 0:
            print(key, ':', temp_map[key])
    if 0 in temp_map:
        print("No path", ':', temp_map[0])


# To ensure that the main method only of this class will be executed.
if __name__ == '__main__':
    main()
