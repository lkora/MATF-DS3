import numpy as np
import random
import math

class System:
    def __init__(self, *args):
        self.n = 0
        self.m = 0
        self.function_result = 0
        self.problem = ""
        self.c = np.array([])
        self.sign_array = np.array([])
        self.A = np.array([])
        self.B = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])
        
        # c A b 
        if len(args[0]) == 3:              
            self.c = args[0][0]
            self.A = args[0][1]
            self.B = args[0][2]

        # otype, c, A, b 
        elif len(args[0]) == 4:
            self.problem = args[0][0]
            self.c = args[0][1]
            self.A = args[0][2]
            self.B = args[0][3]
    
        # otype, c, A, signs, b
        elif len(args[0]) == 5:
            self.problem = args[0][0]
            self.c = args[0][1]
            self.A = args[0][2]
            self.sign_array = args[0][3]
            self.B = args[0][4]
        
        # n, m, otype, in_c, in_A, sign, in_b
        elif len(args[0]) == 7:
            self.n = args[0][0]
            self.m = args[0][1]
            self.problem = args[0][2]
            self.c = args[0][3]
            self.A = args[0][4]
            self.sign_array = args[0][5]
            self.B = args[0][6]

    def find_base_cols(self):
        # Looking for base columns if they exist 
        # B = [-1] * len(self.B)
        B = np.full(self.n, -1)
        for i in range(self.n):
        # Going through rows and looking if there is 1
            for j in reversed(range(len(self.A[i]))):
                if self.A[i, j] == 1:
                    # If it exists we are looking if all the variables in the same column are 0
                    # Creating a list of indexes above and bellow
                    indexes = [l for l in range(len(self.B)) if l!=i]
                    base = all(self.A[l, j]==0 for l in indexes)

                    if base and B[i]==-1:
                        B[i] = j
                        break
        
        return B


    def print_problem(self, list_print=True):
        print(self.problem+' f = ',end='')
        if not list_print:
            for i in range(len(self.c)):
                if self.c[i]!=0:
                    print('{} * x{} '.format(round(self.c[i], 2), i), end='')
        else:
            print([round(i, 2) for i in self.c])
        print()

        for i in range(len(self.A)):
            if not list_print:
                for j in range(len(self.A[i])):
                    if self.A[i, j]!=0:
                        print('{}*x{} '.format(round(self.A[i, j], 2), j), end='')
            else:
                print([round(j, 2) for j in self.A[i]],end='')
            print(' {} {}'.format(self.sign_array[i], round(self.B[i], 2)))
        print()



    def create_sub_problem(self, P):
        # Where there is -1 we add an artificial variable
        # creating a helper problem which we solve by W
        A = self.A.copy()
        c = self.c.copy()
        sign_array = self.sign_array.copy()

        br_prom = len([i for i in P if i==-1])
        c = [0 for i in c]
        c += [1]*br_prom

        new_m = len(A[0])
        zeroes = np.zeros((self.n, br_prom))
        A = np.append(A, zeroes, axis=1)
        # for i in range(len(B)):
        #     A[i] += [0] * br_prom

        # We put 1 where base was -1 because we are adding an artificial variable
        j = 0
        # Puting inedex of artificial variables in a list
        W = []
        for i in range(len(P)):
            if P[i] == -1:
                A[i, new_m+j] = 1
                W.append(new_m+j)
                j += 1
        return System((self.n, self.m, self.problem, c, A, sign_array, self.B)), W


    def simplex(self, max_iter=math.inf):
        print_steps = True
        print_tables = True
        print_python_lists = True
        print_iter = True
        bland_rule = True
        # First looking for the base column
        # If base columns are in a goal function, we have to clean them
        # We put 0 where there is a base column in the goal function 
        # After that we construct the simplex table and begin the algorithm 
        
        B = self.find_base_cols()

        table = self.A
        table = np.append(table, np.reshape(self.B, (len(self.B), 1)), axis=1)
        a = np.append(self.c, [0])
        table = np.vstack((table, np.append(self.c, [0])))
        table = table.tolist()

        if print_steps and print_tables:
            print('Starting table for Simplex:')
            for r in table:
                print([round(i,2) for i in r])
            print()

        # Cleaning the table if any base variable in the goal function has a coefficient different than 0
        # We add a row where that base has a negative coefficient so that we can create 0 in the goal function 
        for i in range(len(B)):
            # The last row has the goal function  -1
            if table[-1][B[i]]!=0:
                coef = -table[-1][B[i]]
                table[-1] = [i+coef*j for i,j in zip(table[-1],table[i])]

        if print_steps and print_tables:
            print('Table for the cleaned goal function: ')
            for r in table:
                print([round(i, 2) for i in r])
            print()

        # We start the simplex after we cleaned the goal function
        iteration = 0
        while True:
            # If tehre is no j such that cj < 0, we found an optimal solution, and we stop 
            if not any(i<0 and i not in B for i in table[-1][:-1]):
                if print_iter:
                    print('Simplex finished in {} iterations.'.format(iteration))
                return B,table
            if iteration>=max_iter:
                break
            # We are looking for j such that cj < 0 and is not in the base
            # If we use Bland's rule we always take the smallest index of the candidate
            # enumerate gives the (i - index, j - value)
            # We skip the last elements since that is the functions value
            candidates = [i for i,j in enumerate(table[-1][:-1]) if j<0 and j not in B]
            ind = candidates[0]
            if not bland_rule:
                ind = random.choice(candidates)
            # We make a list of candidates for the key row around the column pivot
            # Calculate by formula bi/A[i, pivot] where A[i, pivot] > 0
            row = -1
            min = math.inf
            for i in range(len(table)-1):
                if table[i][ind] >0 and table[i][-1]/table[i][ind]<min:
                    min = table[i][-1]/table[i][ind]
                    row = i

            if row == -1:
                print("Simplex error! The column probably doesn't have Aij > 0")

            #sada kada imamo pivot element A[row][ind] pravimo ga bazicnim tako sto iznad i ispod pravimo 0
            #al od njega pravimo jedinicu ceo row delimo sa njim
            table[row] = [i/table[row][ind] for i in table[row]]
            for i in range(len(table)):
                if i!=row:
                    mult = -table[i][ind]
                    table[i] = [i+mult*j for i,j in zip(table[i],table[row])]
            if print_steps and print_tables:
                print('Iteration: {} , pivoting around A[{}, {}]'.format(iteration,row,ind))
                for r in table:
                    print([round(i, 2) for i in r])
                print()
            B[row] = ind
            iteration +=1

        if print_iter:
            print('Warning! Simplex has reached max iterations ({})'.format(max_iter))
        return B,table
