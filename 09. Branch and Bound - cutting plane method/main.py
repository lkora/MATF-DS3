import math
import sys
import numpy as np

from bin.classes.class_system import LinearProblem
from bin.input import input_vars

def main():
    n, m, type_, c, A, sign, b = input_vars()

    b = np.array(b).reshape((n, 1))
    sign = np.array(sign).reshape((n, 1))
    b = np.hstack((sign, b)).tolist()
    for i in range(len(b)):
        b[i][1] = float(b[i][1])
    A = A.tolist()
    c = c.tolist()

    system = LinearProblem(type_, A, b, c)
    system.print_problem()
    print()
    system.gomory_cut()

if __name__ == "__main__":
    main()