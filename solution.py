import numpy as np
from itertools import permutations
from typing import Iterable


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


def calc_subgraphs_edge_weight(weights: list[list[float]], i: int, j: int) -> float:
    sector_size = len(weights) / 3
    i_sector, i_vertices = subgraph_idx_to_original_vertices(sector_size, i)
    j_sector, j_vertices = subgraph_idx_to_original_vertices(sector_size, j)
    if i_sector == j_sector:
        return 0
    result = 0
    result += sum(weights[x][y] for x in i_vertices for y in get_sector_vertices(sector_size, i_sector) - i_vertices)
    result += sum(weights[x][y] for x in i_vertices for y in get_sector_vertices(sector_size, j_sector) - j_vertices)
    result += sum(weights[x][y] for x in j_vertices for y in get_sector_vertices(sector_size, i_sector) - i_vertices)
    return result


def make_subgraphs_adjacency_matrix(weights: list[list[float]]) -> np.array:
    sector_size = len(weights) // 3
    n = 3 * 2 ** sector_size
    result = np.zeroes((n, n))
    for i, j in permutations(range(n), 2):
        result[i, j] = calc_subgraphs_edge_weight(weights, i, j)
    return result


def calc_max_cut(weights: list[list[float]]) -> float:
    while len(weights) % 3 != 0:
        weights.append([0 for _ in range(len(weights))])
        for i in range(len(weights)):
            weights[i].append(0)

    subgraphs_adjacency = make_subgraphs_adjacency_matrix(weights)
    paths3 = subgraphs_adjacency ** 3
    return max(paths3[i, i] for i in paths3.size[0])

    # В каждой трети треугольники должны повторяться, можно сделать так
    # return max(paths3[i, i] for i in paths3.size[0] / 3)
