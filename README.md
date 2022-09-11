# Algebraic Properties
This is a Python code that I developed as a project for the Scientific Programming course delivered by the Politecnico of Milan (M.Sc. in Bioinformatics for computational genomics).

The purpose of this project was to implement both a sequential and a parallel algorithm to test matrices equalities, eventually comparing their performance in terms of time.

## SHORT DESCRIPTION

Usually, given two square matrices A and B it is not true that AB = BA. However, if B=cA, where c is a scalar, then AB=BA.

The required outcome of the project was to implement an algorithm for testing experimentally such hypotheses. It was required to:
1. Take as input a integer N and a scalar c
2. Generate 10 random matrices N*N: A1, A2, .....A10
3. Generate 10 matrices as: B1=cA1, B2=cA2,....B10=cA10
4. Test the equality that Ai = Bi for i = 1, 2, 3, ...., 10
5. Considering a number of threads T > 10, design a second version of the algorithm that uses multiprocessing to speedup the execution.
6. NB: as the number of threads is > 10, assigning each pair of matrices to a single process was not considered a valid solution, as some processes wouldn't have been used.
