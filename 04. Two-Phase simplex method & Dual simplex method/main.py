from bin.classes.class_system import *
from bin.input import input_vars
from bin.revised_simplex_with_ETA import revised_simplex_with_ETA
from bin.canonical_form import canonical_form
from bin.make_standardized_form import make_standardized_form
from bin.print_ import *
from bin.dual_simplex import dual_simplex
from bin.two_phase_simplex import *


def main():
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    option = 0
    while option != 1 and option != 2:
        print("Select one of the possible opions:\n\t(1) Two-Phase simplex method\n\t(2) Dual simplex method")
        option = int(input("Option: "))
        print_split()

    s = System(input_vars())
    if option == 1:
        oproblem = s.problem
        make_standardized_form(s)
        two_phase_simplex(s, problem=oproblem)
    elif option == 2:
        canonical_form(s)
        dual_simplex(s)
    else:
        print("Unknown option selected!")


    

    
if __name__ == '__main__':
   main()
