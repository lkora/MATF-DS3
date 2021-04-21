from .classes.class_system import *
from .del_artifical_vars import del_artifical_vars

import sys
import math
import os


def make_secondary_lp(table):
    problem = 'min'
    A = []
    b = []
    sign_array = []
    c = [i for i in table[-1][:-1]]

    for i in range(len(table)-1):
        A.append([i for i in table[i][:-1]])
        b.append(table[i][-1])
        sign_array.append('=')

    return System((len(A), len(A[0]), problem, np.array(c), np.array(A), np.array(sign_array), np.array(b)))



def two_phase_simplex(Lp, problem="min", print_solution=False):
    func = np.nan
    x = []
    # Will program print (pretty) what is currently doing
    print_steps = False
    # Will program print simplex tables
    print_tables = False
    # Will program print what iteration it is on
    print_iter = False
    # Will program use Bland's rule
    bland_rule = True
    # Will program print just pythonic lists
    print_python_lists = False

    max_iterations = math.inf


    # #ako se prosledi jos jedan argument on sluzi za parametre programa
    # if len(sys.argv)>=3:
    #     print_steps = 'k' in sys.argv[2]
    #     print_tables = 't' in sys.argv[2]
    #     print_iter = 'i' in sys.argv[2]
    #     bland_rule = 'b' in sys.argv[2]
    #     print_python_lists = 'l' in sys.argv[2]

    # #ako se proslede 4 argumenta cetvrti mora da bude max broj iteration za simpleks
    # if len(sys.argv) == 4:
    #     max_iterations = int(sys.argv[3])

    # #ispisujemo stanja programa tj zastavica kako ce ispisivati
    # print('Trenutna konfiguracija programa:')
    # print('Koristi se blendovo pravilo: {}'.format(bland_rule))
    # print('Maximalan broj iteration u simpleksu: {}'.format(max_iterations))
    # print('Format ispisa kao pajton liste: {}'.format(print_python_lists))
    # print('Ipisuju se:')
    # if print_steps:
    #     print('-koraci pri radu')
    # if print_steps and print_tables:
    #     print('-tabele pri iteracijama u simpleksu')
    # if print_iter:
    #     print('-nakon koliko iteration je zavrsen simpleks')
    # print('-finalno resenje')
    # print()

    #vrsimo ucitavanje pocetnog linearnog problema iz tekstualnog fajla
    # Lp = ucitaj_file()

    # if print_steps:
    #     print('Resavamo problem:')
    #     Lp.print_problem(list_print=False)
    #     print('Prebacujemo u standardni oblik')
    #     print()

    #vrsimo standardizaciju pocetnog linearnog problema
    #prebacujemo sve u znak =
    #sve b koji su negativni mnozimo sa -1
    # standard_Lp = Lp.create_canonical_form()

    standard_Lp = Lp
    if print_steps:
        standard_Lp.print_problem()


    # Looking for base columns in standard form 
    B = standard_Lp.find_base_cols()

    if print_steps:
        print('Finding if there is an identity submatrix')
        print('Indexes that can be base columns:')
        print([round(i, 2) for i in B if i != -1])

    # Calculating how many aritificial variables are needed to be added
    num_artificial = len(standard_Lp.B) - len([i for i in B if i!=-1])
    tmp_lp = None

    if num_artificial == 0:
        # If an identitiy submatrix exists we can go straight to simplex
        # No need for two phases
        if print_steps:
            print('Since base matrix can be made from the standard form')
            print('Two phase simplex is not needed')
            print('Solving regular simplex')

        # Doing simplex for the standard form of the problem
        B3, table3 = standard_Lp.simplex()
        func = table3[-1][-1]

        if problem == 'min' and standard_Lp.problem == 'min':
            func *= -1
        
        if print_steps:
            print('Optimal function solution: {}'.format(round(func,2)))
        x = [0] * (len(table3[0]) - 1)

        for i in range(len(standard_Lp.B)):
            x[B3[i]] = table3[i][-1]

        if print_steps:
            print('x = [', end='')
            for i in x:
                print('{} '.format(round(i, 2)), end='')
            print(']')
    else:
        # If it doesn't exist, two phases are needed
        # We are making a tmemporary problem
        tmp_lp,W = standard_Lp.create_sub_problem(B)

        if print_steps:
            print('Since there is no subindentity matrix we add artificial variables')
            print('Number of artificial variables to be added: {}'.format(num_artificial))
            print('Temporary LP:')
            print()
            tmp_lp.print_problem()
            print('Temporary variables we added: {}'.format(W))
            print('Simplex for the temporary problem. START')

        # After we made the temporary problem we start to solve it with simplex
        Bn,table = tmp_lp.simplex()

        # If the result is 0, that means that the original problem has the solution so we start phase two
        if table[-1][-1] == 0:
            if print_steps:
                print()
                print('The result of the temporary problem is 0 => The original problem has a solution')
                print('We take out the added artificial variables')

            # Removing artificial variables
            table2,B2 = del_artifical_vars(table,Bn,W)

            # Changing the last row so that we can add the original goal function
            table2[-1] = np.append(standard_Lp.c, [0])

            if print_steps:
                print()
                print('Cleaned table:')
                for r in table2:
                    print([round(i,2) for i in r])

            # From the new table we create a secondary problem
            secondary_lp = make_secondary_lp(table2)
            if print_steps:
                print()
                print('Seconday LP:')
                secondary_lp.print_problem()
                print()
                print('Simplex over Secondary LP')
                print()

            # Simplex for secondary_lp
            B3,table3= secondary_lp.simplex()
            func = table3[-1][-1]
            if problem == 'min' and secondary_lp.problem=='min':
                func *= -1

            x = [0] * (len(table3[0])-1)
            for i in range(len(secondary_lp.B)):
                x[B3[i]] = table3[i][-1]
            if print_solution:
                print('Optimal function solution: {}'.format(round(func,2)))
                print('x = [',end='')
                for i in x:
                    print('{} '.format(round(i,2)),end='')
                print(']')
        else:
            # If the result was no 0, the original problem has no feasable solution
            if print_solution:
                print('Solution of the temporary function was not 0')
                print('Original problem has no solution!')
            return np.nan, np.nan


    return func, x