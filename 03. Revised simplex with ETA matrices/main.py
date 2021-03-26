from bin.classes.class_system import *
from bin.input import input_vars
from bin.revised_simplex_with_ETA import revised_simplex_with_ETA
from bin.canonical_form import make_canonical_form

# FIX: Equality handling
def main():
    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    s = System(input_vars())
    make_canonical_form(s)
    
    revised_simplex_with_ETA(s)

if __name__ == '__main__':
   main()
