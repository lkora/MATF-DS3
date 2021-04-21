import math

from .print_ import write_table, print_split

Z_set = False

def f_forward(table, i, j):
    if j < 0:
        return -math.inf
    return table[i][j+1]

def reconstruct_forward(table, indexes, solution, A):
    i = len(table) - 2
    j = len(table[i]) - 2 
    global Z_set
    while j > 0:
        print('I{}({}) = {}'.format(len(table)-1,j, indexes[-1][j+1]))
        if Z_set:
            if indexes[-1][j+1]!=0:
                solution[indexes[-1][j+1] - 1] += 1
        else:
            if indexes[-1][j+1]!=0:
                solution[indexes[-1][j+1] - 1] = 1
        i = indexes[-1][j+1]
        print('Weight of {} objecct is {}'.format(indexes[-1][j+1],A[i-1]))
        j-= A[i-1]
        


def knapsack_forward(c, A, b, Z):
    global Z_set
    Z_set = Z

    j = b+2
    n = sum(i!=0 for i in A)

    # Creating a list where a varable that doesn't have a defined weight gets a paremeter
    # If solving for 0/1 Knapsack: If the value is positive -> 1 (since it's max), else 0
    # If solving for Z Knapsack: If the value is positive -> +inf, else 0 (cannot put negative stuff in a box durr)
    tmp = []
    tmp_A = []

    if Z_set:
        tmp =[ math.inf if c[i]>0 and A[i]==0 else 0 for i in range(len(A)) ]
    else:
        tmp =[ 1 if c[i]>0 and A[i]==0 else 0 for i in range(len(A)) ]

    tmp_A = [0] * len(A)
    pom_C = [0] * len(c)

    print()
    for i in range(len(tmp)):
        if tmp[i]!=0:
            tmp_A[i] = A[i] 
            pom_C[i] = c[i]
            print('Variable x{} gets value {} because function has max'.format(i+1,tmp[i]))

    c =[c for c,a in zip(c,A) if a!=0 ]
    A =[a for a in A if a!=0]

    print()
    print('Solving knapsack FORWARDS:')
    print('Forming tables:')
    print()

    # Creating a table
    table =[[0]*j for i in range(n+1)]
    # Making an index table for reconstructing the solution
    indexes =[[0]*j for i in range(n+1)]

    for i in range(1,len(table[0])):
        table[0][i]= i - 1
        indexes[0][i]= i - 1
    
    for i in range(1,len(table)):
        table[i][0] = i
        indexes[i][0] = i

    # If we are working in 0/1 then if the weight of the first object is less than Y
    # we can put it, else if we are working in Z then we put max as much as possible
    for i in range(1,len(table[0])):
        if not Z_set and i-1>=A[0]:
            table[1][i] = c[0]
        elif Z_set:
            table[1][i] = c[0]*((i-1)//A[0])
        if table[1][i]!=0:
            indexes[1][i] = 1

    for i in range(2,len(table)):
        for j in range(1,len(table[i])):

            previous = table[i-1][j]

            k = 1
            if Z_set:
                k = (j-1)//A[i-1]

            value = [f_forward(table,i-1,(j-1)-A[i-1]*l) + c[i-1]*l for l in range(k+1)]

            new_max_value = max(value)

            table[i][j] = max(previous, new_max_value )

            if table[i][j]!=0:
                if previous >= new_max_value:
                    indexes[i][j] = indexes[i-1][j]
                else: 
                    indexes[i][j]= i 
    
    # Filling the table
    table[0][0] ='K\Y'
    indexes[0][0] ='I\Y'

    write_table(table)
    print()
    write_table(indexes)

    solution = [0] * n
    print()
    reconstruct_forward(table,indexes,solution,A)

    for i in range(len(tmp)):
        if tmp[i]!=0:
            solution.insert(i,tmp[i])
            c.insert(i, pom_C[i])
            A.insert(i,tmp_A[i])
    print()
    print('Optimal arrangement is: {}'.format(solution))

    f = sum(i*j for i,j in zip(solution,c) if i!=math.inf )


    print('Optimal value is: {} '.format(f),end='')
    if any(i==math.inf for i in solution):
        print('+ {}'.format(math.inf))

    print_split()