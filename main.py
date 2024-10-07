from collections import defaultdict
from itertools import product
from pprint import pprint
from random import randint
import numpy


def get_input(filename) -> tuple[int, dict]:
    """tutte_d[v1, v2] -> {vi, ... vj}"""
    with open(filename) as f:
        n, *edges_ = f.readlines()
        edges_rl, edges_lr = defaultdict(set), defaultdict(set)
        for src, target in map(str.split, edges_):
            edges_lr[int(src)].add(target)
            edges_rl[target].add(int(src))

        l_to_l_d = defaultdict(set)
        for key, val in edges_lr.items():
            for r_vertice in val:
                for l_vertice_target in edges_rl[r_vertice]:
                    if key == l_vertice_target:
                        continue

                    l_to_l_d[key, l_vertice_target].add(r_vertice)

        return int(n), l_to_l_d


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


def sub_to_matrix(variables: set, test_vector: dict, mask: set, matrix: list) -> list:
    n = len(matrix)
    tutte_m_filled_ = list(list(0 for __ in range(n)) for _ in range(n))
    for i, j in product(range(n), range(n)):
        tutte_m_filled_[i][j] = sum((test_vector[var] if variables[var] in mask else 0) for var in matrix[i][j])
        # tutte_m_filled_[i][j] = sum((test_vector[var]) for var in matrix[i][j])
    tutte_m_filled = numpy.array(tutte_m_filled_)
    # print('Sub to matrix mask: ')
    # pprint(mask)
    # print('Sub to matrix test_vec: ')
    # pprint(test_vector)
    # print('Sub to matrix response: ')
    # pprint(tutte_m_filled)
    return tutte_m_filled


def determinant(matrix_filled: list) -> bool:
    return numpy.linalg.det(matrix_filled)


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
    vertices_amount, tutte_d = get_input('input.txt')
    print('L to L d:', *tutte_d.items(), sep='\n')
    variables, tutte_m = generate_tutte_matrix(vertices_amount, tutte_d)
    print('Tutte matrix:')
    pprint(tutte_m)
    # print('variables:')
    # pprint(variables)
    # for _ in range(100):
    #     test_vector = generate_random_vector(variables)
    #     # test_vector = {val: 1 for val in variables}
    #
    #     print(sum_all_perms(variables, test_vector, set(variables.values()), tutte_m), end=' ')
    #

    for _ in range(100):
        test_vector = generate_random_vector(variables)
        if sum_all_perms(variables, test_vector, set(variables.values()), tutte_m):
            print('yes')
            break
    else:
        print('no')
