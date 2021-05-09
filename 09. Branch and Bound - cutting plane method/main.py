from bin.classes.class_system import System
from bin.input import input_vars
from bin.print_ import print_split
from bin.branch_and_bound import branch_and_bound

def main():
    s = System(input_vars())
    branch_and_bound(s)

if __name__ == '__main__':
    main()
