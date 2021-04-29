import math

from ..print_ import print_number, print_variable, print_simplex_table
from ..clean_artificial import clean_from_artificial
from ..dual_simplex import dual_simplex
from ..table_simplex import table_simplex

decimal_space = 2

def fraction_part(a):
    if a>=0:
        return abs(a) - math.floor(abs(a))
    else :
        b = abs(a)
        b = math.ceil(b)
        return b - abs(a)
    

class LinearProblem:
    # Linear problem class
    def __init__(self,type,A,b,Z):
        self.type = type
        self.A = A.copy()
        for i in range(len(A)):
            self.A[i] = A[i].copy()
        self.b = b.copy()
        self.Z = Z.copy()


    def print_problem(self):
        print(self.type,end=' ')
        print(self.Z)
        print()
        for i in range(len(self.b)):
            print(self.A[i],end=' ')
            print(self.b[i][0],end=' ')
            print(self.b[i][1])
    
    # Standardize problem
    def standardize(self):
        if self.type == 'max':
            self.Z = [-i for i in self.Z]
    # If any of b < 0 we multiply the whole row by -1 and flip the sign
        for i in range(len(self.b)):
            if self.b[i][1]<0:
                self.A[i] = [-j for j in self.A[i] ]
                self.b[i][1] = -self.b[i][1]
                if self.b[i][0] =='<=':
                    self.b[i][0] = '>='
                elif self.b[i][0] =='>=':
                    self.b[i][0] = '<='


        # Adding flattening variables
        # If <= we add +s
        # If >= we add -s
        # if >= and b is 0, we multiply by -1 and add +s
        S =[]
        for i in range(len(self.b)):
            # For all others that are not in the row we add 0
            if self.b[i][0] != '=':
                for j in range(len(self.b)):
                    if j!=i:
                        self.A[j].append(0.0)
            if self.b[i][0] == '<=':
                self.A[i].append(1.0)
                S.append(len(self.A[i])-1)
                self.Z.append(0.0)
            elif self.b[i][0] == '>=' and self.b[i][1]==0 :
                self.A[i] = [-a for a in self.A[i]]
                self.A[i].append(1.0)
                S.append(len(self.A[i])-1)
                self.Z.append(0.0)
            elif self.b[i][0] == '>=':
                self.A[i].append(-1.0)
                S.append(len(self.A[i])-1)
                self.Z.append(0.0)
            self.b[i][0] = '='
        return S


    def find_base(self):
        # Going backwards and looking if there is 0...1...0 to become the base for a row
        B = [-1] * len(self.b)
        for i in reversed(range(len(self.A[0]))):
            for j in range(len(self.b)):
                if self.A[j][i] == 1 and all(self.A[k][i]==0 for k in range(len(self.b)) if k!=j ) and B[j]==-1:
                    B[j] = i
        return B

    def add_artificial(self, B):
        W = []
        for i in range(len(B)):
            if B[i] == -1:
                for j in range(len(self.b)):
                    if j!=i:
                        self.A[j].append(0.0)
                self.A[i].append(1.0)
                B[i] = len(self.A[i]) - 1
                W.append(len(self.A[i]) - 1)
                self.Z.append(0.0)
        return B,W

    def make_simplex_table(self):
        table = []
        for i in range(len(self.b)):
            table.append(self.A[i].copy())
            table[i].append(self.b[i][1])
        table.append(self.Z.copy())
        table[-1].append(0.0)
        return table
                

    def two_phase_simplex(self):
        print('Standardizing problem:')
        S = self.standardize()
        self.print_problem()
        print()
        print()
        print('Looking for base colmuns:')
        B = self.find_base()
        print(B)
        print()
        old_Z = self.Z.copy()
        if any(i==-1 for i in B):
            print('Not enough base variables, adding artificial:')
            B,W = self.add_artificial(B)
            print()
            print('Temporary problem is:')
            self.Z = [0.0 for i in self.Z]
            for w in W:
                self.Z[w] = 1.0
            self.print_problem()
            print()
            print('Starting table simplex for phase 1:')
            print()
            table, B = table_simplex(self.make_simplex_table(), B, S, W)
            if table!= None:
                if table[-1][-1] == 0:
                    print('Solution is 0 => there is a solution for the starting problem')
                    table, B = clean_from_artificial(table,B,W)
                    print('Table cleaned from artificial variables: ')
                    table[-1] = old_Z.copy()
                    table[-1].append(0.0)
                    print()
                    table ,B = table_simplex(table,B,S,W)
                    f = 0.0
                    x = [0.0] * (len(table[0])-1)
                    for b in B:
                        ind = B.index(b)
                        x[b] = table[ind][-1]
                        f += x[b] * old_Z[b]
                    print('Optimal x is: {}'.format([round(j,decimal_space) if not round(j,decimal_space).is_integer() else int(j) for j in x]))
                    if self.type == 'max':
                        f = -f
                    if round(f,decimal_space).is_integer():
                        print('F {} = {}'.format(self.type,int(round(f,decimal_space))))
                    else:
                        print('F {} = {}'.format(self.type,round(f,decimal_space)))
                    return table,x,f,B
                else:
                    print('Solution is not 0 => there is no solution for the starting problem')
                    return None , [] , 0 , B
            else:
                return None , [] , 0 , B

        else:
            print('There are enough base variables, solving with simplex:')
            print()
            table , B = table_simplex(self.make_simplex_table(),B,S,[])
            if table!= None:
                    f = 0.0
                    x = [0.0] * (len(table[0])-1)
                    for b in B:
                        ind = B.index(b)
                        x[b] = table[ind][-1]
                        f += x[b] * old_Z[b]
                    print('Optimal x is: {}'.format([round(j,decimal_space) if not j.is_integer() else int(j) for j in x]))
                    if self.type == 'max':
                        f = -f
                    if round(f,decimal_space).is_integer():
                        print('F {} = {}'.format(self.type,int(round(f,decimal_space))))
                    else:
                        print('F {} = {}'.format(self.type,round(f,decimal_space)))
                    return table,x,f,B
            else:
                return None , [] , 0 , B

    def add_solution(self, table, B):
        ind = -1

        for i in range(len(table)):
            if round(table[i][-1],decimal_space).is_integer() == False:
                ind = i
                break
            
        if ind == -1:
            print('Did not find a non integer row')
            quit()

        print("{} row doesn't have an integer solution so we create a result:".format(ind))
        create_row = [fraction_part(a) for a in table[ind][:-1]]
        new_right_side = fraction_part(table[ind][-1])
        print('\nNew inequation: ')
        print([ int(round(a,decimal_space)) if round(a,decimal_space).is_integer() else round(a,decimal_space) for a in create_row ],end=' >= ')
        print(round(new_right_side, decimal_space))
        
        create_row = [-a for a in create_row]
        create_row.append(1.0)
        new_right_side = -new_right_side
        create_row.append(new_right_side)

        for i in range(len(table)):
            table[i].insert(-1,0.0)

        table.insert(-1,create_row)
        B.append(len(table[0])-2)


    def gomory_cut(self):
        print("Starting Gomory cut algorithm")
        print("First we solve the two phase simplex for the initial problem")
        print()
        old_Z = [i for i in self.Z]
        table, x, f, B = self.two_phase_simplex()
        number_of_cuts = 0
        print()

        while not all( round(row[-1],decimal_space).is_integer() for row in table ):
            # print(colorow('+++++++++++++++++++++++++++++++++++++++++++++++++','blue'))
            print("Solution is not an integer, we need to do a gomory cut:")
            self.add_solution(table,B)
            number_of_cuts +=1

            print()
            print('After adding an inequality, we get a table:')
            print_simplex_table(table, B, [], [])
            print()
            print('Starting the dual simplex:')
            table, B = dual_simplex(table,B)

        print()
        # print(colorow('+++++++++++++++++++++++++++++++++++++++++++++++++','blue'))
        print("Solution is an integer => We stop plane cutting!!!")
        print("Number of cuts made: {}".format(number_of_cuts))
        print()
        f = 0.0
        x = [0.0] * (len(old_Z))
        
        for b in B:
            if b<len(old_Z):
                ind = B.index(b)
                x[b] = table[ind][-1]
                f += x[b] * old_Z[b]

        print('Optimal x is: {}'.format([round(j,decimal_space) if not j.is_integer() else int(j) for j in x]))
        if round(f,decimal_space).is_integer():
            print('F{} = {}'.format(self.type,int(round(f,decimal_space))))
        else:
            print('F {} = {}'.format(self.type,round(f,decimal_space)))
