from itertools import product
from pprint import pprint

import numpy as np

graph_g = set()
POWER = 0


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


def count_weight_for_vertex_pair(vertex1, shift_1, vertex2, shift_2):
    included = set(
        index + shift_1 for index, bit in
        enumerate(f'{vertex1:b}'.ljust(POWER, '0')) if bit == '1'
    )
    excluded = set(
        index + shift_2 for index, bit in
        enumerate(f'{vertex2:b}'.ljust(POWER, '0')) if bit == '0'
    )

    answer = sum(
        1 for pair in product(
            included,
            excluded
        ) if tuple(sorted(pair)) in graph_g)

    return answer


def invert_bits(num):
    mask = (1 << POWER) - 1  # Создаем маску из всех единиц длиной k бит
    return ~num & mask  # Инвертируем биты числа и обрезаем до k бит


def get_matrix_h(n):
    combinations_amount = 2 ** POWER
    matrix_h = np.zeros((3 * combinations_amount, 3 * combinations_amount), dtype=int)
    # todo: починить этот обосравшийся цикл
    for sector, vertex in product(range(3), range(combinations_amount)):
        shift_src = sector * POWER
        weight_inside_sector = count_weight_for_vertex_pair(
            vertex, shift_src, vertex, shift_src
        )

        shift_trg = ((sector + 1) % 3) * POWER
        src_to_trg = 0
        for combo in range(combinations_amount):
            src_to_trg += count_weight_for_vertex_pair(
                vertex, shift_src, combo, shift_trg
            )
            src_to_trg += count_weight_for_vertex_pair(
                combo, shift_trg, vertex, shift_src
            )
            row, column = vertex + shift_src, combo + shift_trg
            weight = src_to_trg + weight_inside_sector

            matrix_h[row, column] = weight if weight else -1
            matrix_h[column, row] = weight if weight else -1

    return matrix_h


def main():
    global POWER
    with open("input.txt") as f:
        n, *data = f.readlines()

    n = int(n)
    n += 3 - n % 3  # Добавляем вершины до кратности 3,
    # Чтобы равномерно разбить их на соответствующие участки
    POWER = n // 3

    for src, target in (tuple(map(lambda x: int(x) - 1, line.split())) for line in data):
        graph_g.add((min(src, target), max(src, target)))

    matrix_h = get_matrix_h(n)
    pprint(matrix_h)
    return


if __name__ == '__main__':
    main()
