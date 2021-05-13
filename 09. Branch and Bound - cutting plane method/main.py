import matplotlib.pyplot as plt
import numpy as np

from bin.classes.class_system import System
from bin.input import input_vars
from bin.print_ import print_split
from bin.branch_and_bound import branch_and_bound


def plot_2_d(s, x_opt):
    if s.m == 2:
        x = np.linspace(0, 20, 100)
        y = []
        for i in range(s.n):
            if s.A[i][1] != 0:
                y.append((s.b[i]-s.A[i][0]*x)/s.A[i][1])
                plt.plot(x, y[i], 'r')
            else:
                y.append((s.b[i]-s.A[i][1]*x)/s.A[i][0])
                plt.plot(x, y[i], 'b-', label="x"+str(i))
        plt.xlim(0, x_opt[0]*5)
        plt.ylim(0, x_opt[1]*5)
        plt.plot(x_opt[0], x_opt[1], 'gs')
        plt.xlabel(r'$x$')
        plt.ylabel(r'$y$')
        plt.show()



def main():
    s = System(input_vars())
    f_opt, x_opt = branch_and_bound(s)
    plot_2_d(s, x_opt)


if __name__ == '__main__':
    main()
