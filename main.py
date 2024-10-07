from collections import defaultdict
from itertools import product
from pprint import pprint
from random import randint
import numpy


def get_input(filename) -> tuple[set, set, dict]:
    """tutte_d[v1, v2] -> {vi, ... vj}"""
    with open(filename) as f:
        n, *edges_ = f.readlines()
        edges_rl, edges_lr = defaultdict(set), defaultdict(set)
        for src, target in map(str.split, edges_):
            edges_lr[int(src)].add(target)
            edges_rl[target].add(int(src))

        l_to_l_d = defaultdict(set)
        l_vertices_ = set()
        r_vertices_ = set()
        for key, val in edges_lr.items():
            l_vertices_.add(key)
            for r_vertice in val:
                r_vertices_.add(r_vertice)
                for l_vertice_target in edges_rl[r_vertice]:
                    if key == l_vertice_target:
                        continue

                    l_to_l_d[key, l_vertice_target].add(r_vertice)

        return l_vertices_, r_vertices_, l_to_l_d


def generate_tutte_matrix(n: int, graph: dict):
    all_vars = dict()

    tutte_m = list(list([] for __ in range(n // 2)) for _ in range(n // 2))
    for i, j in product(range(n // 2), range(n // 2)):
        i_, j_ = str(i), str(j)
        if i == j:
            continue
        for r_vertice in graph[i, j]:
            mark = '!' if j == 0 else ''
            variable = '-'.join([r_vertice, min(i_, j_), max(i_, j_)]) + mark
            tutte_m[i][j].append(variable)
            all_vars[variable] = r_vertice
    return all_vars, tutte_m


def generate_random_vector(variables: set):
    result = {key: randint(0, 1) for key in variables}
    return result


def det(m):
    m = [row[:] for row in m]  # make a copy to keep original M unmodified
    n, sign, prev = len(m), 1, 1
    for i in range(n - 1):
        if m[i][i] == 0:  # swap with another row having nonzero i's elem
            swapto = next((j for j in range(i + 1, n) if m[j][i] != 0), None)
            if swapto is None:
                return 0  # all M[*][i] are zero => zero determinant
            m[i], m[swapto], sign = m[swapto], m[i], -sign
        for j in range(i + 1, n):
            for k in range(i + 1, n):
                assert (m[j][k] * m[i][i] - m[j][i] * m[i][k]) % prev == 0
                m[j][k] = (m[j][k] * m[i][i] - m[j][i] * m[i][k]) // prev
        prev = m[i][i]
    return sign * m[-1][-1]


def sub_to_matrix(variables: set, test_vector: dict, mask: set, matrix: list) -> list:
    n = len(matrix)
    tutte_m_filled = numpy.zeros((n, n), dtype=int)
    for i, j in product(range(n), range(n)):
        tutte_m_filled[i, j] = sum((test_vector[var] if variables[var] in mask else 0) for var in matrix[i][j])
        # tutte_m_filled_[i][j] = sum((test_vector[var]) for var in matrix[i][j])
    # print('Sub to matrix mask: ')
    # pprint(mask)
    # print('Sub to matrix test_vec: ')
    # pprint(test_vector)
    # print('Sub to matrix response: ')
    # pprint(tutte_m_filled)
    return tutte_m_filled


def determinant(matrix_filled: list) -> bool:
    return det(matrix_filled)


def combinations_gen(vertices):
    import itertools
    for i in range(1, len(vertices) + 1):
        for combination in itertools.combinations(vertices, i):
            yield set(combination)


def sum_all_perms(variables, test_vector, vertices, tutte_m):
    iterator = combinations_gen(vertices)
    answer = 0
    for mask in iterator:
        answer += determinant(sub_to_matrix(variables, test_vector, mask, tutte_m))
    return answer % 2


if __name__ == '__main__':
    l_vertices, r_vertices, tutte_d = get_input('input.txt')
    # print('L to L d:', *tutte_d.items(), sep='\n')
    variables, tutte_m = generate_tutte_matrix(len(l_vertices) + len(r_vertices), tutte_d)
    # print('Tutte matrix:')
    # pprint(tutte_m)
    # print('variables:')
    # pprint(variables)
    # for _ in range(100):
    #     test_vector = generate_random_vector(variables)
    #     # test_vector = {val: 1 for val in variables}
    #
    #     print(sum_all_perms(variables, test_vector, set(variables.values()), tutte_
    #     m), end=' ')

    for _ in range(10000):
        test_vector = generate_random_vector(variables)
        if sum_all_perms(variables, test_vector, r_vertices, tutte_m):
            print('yes')
            break
    else:
        print('no')
