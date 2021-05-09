from bin.classes.class_system import System
from bin.input import input_vars
from bin.print_ import print_split, write_table, print_initial
from bin.knapsack_forward import knapsack_forward
from bin.knapsack_backward import knapsack_backward


def main():
    s = System(input_vars())
    
    print('Loaded the problem:\n')
    print('max {}'.format(s.c))
    print('    {} <= {}'.format(s.A, s.b))
    
    # Get the inputed set and print the initial problem
    Z_set = False
    if s.solution_set.lower() == 'z':
        Z_set = True
    print_initial(Z_set)

    if s.direction == 'forward':
        knapsack_forward(s.c, s.A, s.b, Z_set)
    else:
        knapsack_backward(s.c, s.A, s.b, Z_set)

if __name__ == '__main__':
   main()