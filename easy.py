from itertools import permutations, combinations

import numpy as np


def get_sector_vertices(sector_size: int, sector_idx: int) -> set[int]:
    return set(range(sector_idx * sector_size, (sector_idx + 1) * sector_size))


def subgraph_idx_to_original_vertices(sector_size: int, idx: int) -> tuple[int, set[int]]:
    subgraphs_sector_size = 2 ** sector_size
    sector_idx = idx // subgraphs_sector_size
    in_sector_idx = idx - subgraphs_sector_size * sector_idx
    result = set(index for index, bit in enumerate(bin(in_sector_idx)[2:]) if bit == '1')
    # in_sector_idx - битовая маска, в которой
    # бит i обозначает вхождение вершины (sector_idx * sector_size + i)
    # в множество с номером idx
    # TODO: заполнить result
    return sector_idx, result


def calc_subgraph_edge_weight(weights: list[list[float]], i: int, j: int) -> float:
    sector_size = len(weights) // 3
    i_sector, i_vertices = subgraph_idx_to_original_vertices(sector_size, i)
    j_sector, j_vertices = subgraph_idx_to_original_vertices(sector_size, j)
    if i_sector == j_sector:
        return 0
    result = 0
    result += sum(weights[x][y] for x in i_vertices for y in get_sector_vertices(sector_size, i_sector) - i_vertices)
    result += sum(weights[x][y] for x in i_vertices for y in get_sector_vertices(sector_size, j_sector) - j_vertices)
    result += sum(weights[x][y] for x in j_vertices for y in get_sector_vertices(sector_size, i_sector) - i_vertices)
    return result


# Это написано неправильно
# def count_sub_weight_for_vertex(length, vertex, graph_g, n_subset=0):
#     """
#     Считаем вес в рамках одной кучи для вершины и её отрицания. w(x1, y1)
#     :param graph_g:
#     :param length:
#     :param vertex:
#     :return:
#     """
#     included = set(index for index, bit in enumerate(f'{vertex: b}'.ljust(length, '0')) if bit == '1')
#
#     weight = 0
#
#     for i in range(length):  #
#         if i in included:
#             continue
#         weight += sum([(length * n_subset + i, length * n_subset + j) in graph_g for j in range(length)])
#     return weight

def count_weight_for_vertex_pair(vertex1, n_sub1, vertex2, n_sub2):
    included = set(index for index, bit in enumerate(f'{vertex1: b}'.ljust(vertex1, '0')) if bit == '1')
    excluded = set(index for index, bit in enumerate(f'{vertex2: b}'.ljust(vertex2, '0')) if bit == '0')
    pass


def get_matrix_h(n, matrix_g):
    combinations_amount = 2 ** (len(matrix_g) // 3)
    matrix_h = np.zeros((3 * combinations_amount, 3 * combinations_amount), dtype=int)

    for vertex in combinations_amount:
        weight = count_weight_for_vertex_pair((len(matrix_g) // 3), vertex, graph_g)

    answer = list()
    return answer


def main():
    with open("input.txt") as f:
        n, *data = f.readlines()

    n = int(n)
    n += 3 - n % 3  # Добавляем вершины до кратности 3,
    # Чтобы равномерно разбить их на соответствующие участки

    # adj_matrix = np.zeros((n, n), dtype=int)
    # for src, target in (tuple(map(int, line.split())) for line in data):
    #     adj_matrix[src - 1, target - 1] = 1
    #     adj_matrix[target - 1, src - 1] = 1
    graph_g = set()
    for src, target in (tuple(map(int, line.split())) for line in data):
        graph_g.add((min(src, target), max(src, target)))

    matrix_h = get_matrix_h(n, graph_g)
