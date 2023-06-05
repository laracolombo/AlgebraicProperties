# PROJECT 8: Algebraic Properties
# Scientific Programming course, A.Y. 2021/2022
# Colombo Lara, matriculation number 995885, person code 10650585

import functools
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ALGEBRAIC PROPERTIES

# Usually, given two square matrices A and B it is not true that AB = BA.
# However, if B=cA, where c is a scalar, then AB=BA.

# The purpose of this project is to implement both a sequential and a parallel algorithm to test such hypothesis,
# eventually comparing their performance in terms of time.

# First, the user can pick the integer number N that determines the dimension of the NxN square matrices:
n = int(input(f'Write here an integer number N: '))
# then, also the scalar number c can be chosen:
c = round(float(input(f'Write here a scalar number c: ')), 3)

# NOTE: to get a real difference in terms of performance, and in particular to actually gain an execution speedup
# by multiprocessing, passing large values of N is advised.
# In fact, employing multiprocess to manage data of small size might not be worth, due to the overhead of creating
# new processes that can be larger than the computing the result itself.

# SEQUENTIAL ALGORITHM

start = time.time()

for i in range(10):
    matrix_a = np.random.random((n, n))  # generate a NxN matrix Ai with random numbers
    matrix_b = matrix_a * c  # generate a matrix Bi in the form Bi = cAi
    # compare the matrix multiplication AiBi to the matrix multiplication BiAi
    a = np.round(np.dot(matrix_a, matrix_b), 3) == np.round(np.dot(matrix_b, matrix_a), 3)
    # check that TRUE was returned for each element in the comparison
    if False in a:
        print(f'SEQUENTIAL: Error: A{i + 1}B{i + 1} is different from B{i + 1}A{i + 1}')
    else:
        print(f'SEQUENTIAL: The equality A{i + 1}B{i + 1} = B{i + 1}A{i + 1} was verified!')

end = time.time()

print(f'Timing of sequential algorithm: {end - start}')


# PARALLEL ALGORITHM

# The second version of the algorithm was implemented by introducing multiprocessing.
# In particular, a pool of worker threads (for a total of 12 threads) was employed to run instances in parallel (or
# better, concurrently) by importing the ThreadPool module.
# I decided to rely on threads instead of processes because the latter usually generate more system overhead and it
# wasn't worth for such a simple computation as the comparison of two matrices, as I verified myself during the
# development of the code.

# defining an helper function to generate random matrices, which will be used in the main() function
def random_matrix(_, n):
    return np.random.random((n, n))


# defining a function to generate 10 random matrices in parallel through a Pool of 6 working threads
def main():
    with ThreadPool(6) as pool:
        return list(pool.imap(functools.partial(random_matrix, n=n), [1, 1] * 5))  # returns a list of 10 matrices


# defining a function to test the equality between a matrix Ai and a matrix Bi = cAi
# m is a two-elements list storing one integer number (which is the index i) and one matrix Ai, in the form (idx, Ai)
def test_equality(m, c):
    idx = m[0]  # getting the index i of the matrix Ai
    matrix_b = m[1] * c  # generating the matrix Bi in the form Bi = cAi
    # compare the matrix multiplication AiBi to the matrix multiplication BiAi
    a = np.round(np.dot(m[1], matrix_b), 3) == np.round(np.dot(matrix_b, m[1]), 3)
    # check that TRUE was returned for each element in the comparison
    if False in a:
        print(f'PARALLEL: Error: A{idx + 1} * B{idx + 1} is different from B{idx + 1} * A{idx + 1}')
    else:
        print(f'PARALLEL: The equality A{idx + 1}B{idx + 1} = B{idx + 1}A{idx + 1} was verified!')


if __name__ == "__main__":
    start = time.time()

    # add a counter (= index i) to each element of the list returned by main(), obtaining a list of
    # 2-elements lists in the form (idx, matrix)
    matrices = list(enumerate(main()))

    # generating a Pool of 6 working threads to test the equality between each matrix Ai in 'matrices' and their
    # corresponding matrix Bi
    b = ThreadPool(6)
    b.map(functools.partial(test_equality, c=c), matrices)

    end = time.time()

    print(f'Timing of the parallel algorithm: {end - start}')

# GRAPHIC VISUALIZATION AND PERFORMANCE COMPARISON

# As mentioned before, if N is not big enough, the overhead of creating (12) new processes will be more
# expensive than computing the actual results, resulting in a slowdown of the parallel code instead of a speedup.

# The following code is meant to show how the performances of the two algorithms change as N increases, leading the
# parallel version to outperform the sequential one only for big values of N.

c = 1.273  # arbitrary value for the scalar number c

sequential_timing = []
parallel_timing = []

if __name__ == "__main__":

    for n in [2500, 3500, 4500]:  # arbitrary values for the integer number N

        start = time.time()
        matrices = list(enumerate(main()))

        b = ThreadPool(6)
        b.map(functools.partial(test_equality, c=c), matrices)

        end = time.time()

        parallel_timing.append(end-start)

        start_s = time.time()

        for x in range(10):
            matrix_a = np.random.random((n, n))
            matrix_b = matrix_a * c
            a = np.round(np.dot(matrix_a, matrix_b), 3) == np.round(np.dot(matrix_b, matrix_a), 3)
            if False in a:
                print(f'SEQUENTIAL: Error: A{x + 1}B{x + 1} is different from B{x + 1}A{x + 1}')
            else:
                print(f'SEQUENTIAL: The equality A{x + 1}B{x + 1} = B{x + 1}A{x + 1} was verified!')

        end_s = time.time()

        sequential_timing.append(end_s-start_s)

    # Generating the graph

    L = sequential_timing + parallel_timing
    df = pd.DataFrame({'seconds': L})
    df['type'] = ["sequential", "sequential", "sequential", "parallel", "parallel", "parallel"]
    df['dimensions'] = ["2500", '3500', '4500'] * 2
    print(df)
    sns.barplot(x="dimensions", y= "seconds", hue="type", data=df)

    # Show the plot

    plt.show()
