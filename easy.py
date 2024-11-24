from itertools import product
from pprint import pprint

import numpy as np
from numpy import ndarray

graph_g = set()
POWER = 0

MASK = 0  # (1 << POWER) - 1  # Создаем маску из всех единиц длиной k бит


def invert_bits(num):
    return ~num & MASK  # Инвертируем биты числа и обрезаем до k бит


def count_weight_for_vertex_pair(vertex1, shift_1, vertex2, shift_2):
    incl_bin_set = list(enumerate("".join(reversed(f'{vertex1:b}')).ljust(POWER, '0')))
    excl_bin_set = list(enumerate("".join(reversed(f'{vertex2:b}')).ljust(POWER, "0")))
    included = set(
        index + shift_1 for index, bit in incl_bin_set if bit == '1'
    )
    excluded = set(
        index + shift_2 for index, bit in excl_bin_set if bit == '0'
    )
    answer = sum(1 for pair in product(included, excluded) if pair in graph_g)

    return answer


def get_matrix_h(n):
    combinations_amount = 2 ** POWER
    matrix_h = np.zeros((3 * combinations_amount, 3 * combinations_amount), dtype=int)

    for sector, vertex in product(range(3), range(combinations_amount)):
        vertex_shift = sector * POWER
        weight_inside_sector = count_weight_for_vertex_pair(
            vertex, vertex_shift, vertex, vertex_shift
        )

        combo_shift = ((sector + 1) % 3) * POWER
        for combo in range(combinations_amount):
            row, column = (vertex + sector * combinations_amount, combo + ((sector + 1) % 3) * combinations_amount)
            src_to_trg = count_weight_for_vertex_pair(
                vertex, vertex_shift, combo, combo_shift
            )
            src_to_trg += count_weight_for_vertex_pair(
                combo, combo_shift, vertex, vertex_shift
            )
            weight = src_to_trg + weight_inside_sector

            matrix_h[row, column] = weight
            matrix_h[column, row] = weight

    return matrix_h


def get_cleansed_matrix(matrix: ndarray, val1, val2, val3):
    combinations_amount = 2 ** POWER
    answer = matrix.copy()
    for sector, vertex in product(range(3), range(combinations_amount)):
        value = [val1, val2, val3][sector]
        for combo in range(combinations_amount):
            row, column = (vertex + sector * combinations_amount, combo + ((sector + 1) % 3) * combinations_amount)
            answer[row, column] = value if answer[row, column] == value else 0
            answer[column, row] = value if answer[column, row] == value else 0

    return answer


def main():
    global POWER, MASK
    with open("classical.txt") as f:
        n, *data = f.readlines()

    n = int(n)
    n += 3 - n % 3  # Добавляем вершины до кратности 3,
    # Чтобы равномерно разбить их на соответствующие участки
    POWER = n // 3
    MASK = (1 << POWER) - 1  # Создаем маску из всех единиц длиной k бит

    for src, target in (tuple(map(lambda x: int(x) - 1, line.split())) for line in data):
        graph_g.add((src, target))
        graph_g.add((target, src))

    matrix_h = get_matrix_h(n)

    edges = len(graph_g) // 2
    max_cut = 0
    for v1, v2, v3 in product(range(1, edges + 1), range(1, edges + 1), range(1, edges + 1)):
        cleansed_h = get_cleansed_matrix(matrix_h, v1, v2, v3)
        powered = np.linalg.matrix_power(cleansed_h, 3)
        max_cut = max(max_cut, (v1 + v2 + v3) * powered.any())

    return max_cut


if __name__ == '__main__':
    print(main())
