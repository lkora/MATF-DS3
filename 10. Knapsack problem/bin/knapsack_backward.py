import math

from .print_ import write_table, print_split


def f_backward(memo, c, A, b, i, j):

    if i<0 or j<0:
        return -math.inf
    
    if memo[i][j]!=-math.inf:
        if i==1:
             print('F{}({}) = {}'.format(i,j-1,memo[i][j]))
        return memo[i][j]

    global Z_set

    k = 1
    if Z_set:
        k = j//A[i-1]
    
    print('F{}({}) = max['.format(i,j-1),end='')

    for l in range(k+1):
        if (j-1)-A[i-1]*l>=0:
            print(' {} + F{}({}) ,'.format( c[i-1]*l , i-1 , (j-1)-A[i-1]*l ),end='')
    print(']\n')

    possible_solutions = [ c[i-1]*l+f_backward(memo,c,A,b,i-1,j-A[i-1]*l) for l in range(k+1) if (j-1)-A[i-1]*l>=0]

    max_value = max(possible_solutions)

    memo[i][j] = max_value

    return max_value

def reconstruct_backward(memo, i, j, A, c, solution):
    if i < 0 or j < 0:
        return
    
    global Z_set

    k = 1
    if Z_set:
        k = j//A[i-1]

    possible_solutions = [ c[i-1]*l+memo[i-1][j-A[i-1]*l] for l in range(k+1) if (j-1)-A[i-1]*l>=0]
    print(possible_solutions)
    max_value = max(possible_solutions)
    ind = possible_solutions.index(max_value)
    print(ind)
    solution[i-1] += ind
    reconstruct_backward(memo, i-1, j-A[i-1]*ind, A, c, solution)

def knapsack_backward(c, A, b, Z):
    global Z_set
    Z_set = Z

    j = b
    n = sum(i!=0 for i in A)
    # Creating a list where a varable that doesn't have a defined weight gets a paremeter
    # If solving for 0/1 Knapsack: If the value is positive -> 1 (since it's max), else 0
    # If solving for Z Knapsack: If the value is positive -> +inf, else 0 (cannot put negative stuff in a box durr)

    tmp = []
    tmp_A = [0] * len(A)
    pom_C = [0] * len(c)

    if Z_set:
        tmp =[ math.inf if c[i]>0 and A[i]==0 else 0 for i in range(len(A)) ]
    else:
        tmp =[ 1 if c[i]>0 and A[i]==0 else 0 for i in range(len(A)) ]

    print()
    for i in range(len(tmp)):
        if tmp[i]!=0:
            tmp_A[i] = A[i]
            pom_C[i] = c[i]
            print('Variable x{} gets value {} because function has max'.format(i+1,tmp[i]))
    print()
    print('Solving knapsack BACKWARDS:')
    print()

    c =[c for c,a in zip(c,A) if a!=0 ]
    A =[a for a in A if a!=0]
    
    # Making memoization for easier calculation
    memo = [[-math.inf] * (j+2) for i in range(n+1)]

    solution = [0] * n
    for i in range(1,len(memo[0])):
        memo[0][i] = i-1
    for i in range(1,len(memo)):
        memo[i][0] = i
    memo[0][0] = 'K\Y'

    # Setting initial values
    for i in range(1,len(memo[1])):
        if Z_set:
            memo[1][i] = c[0]*((i-1)//A[0])
        else:
            if i>=A[0]:
                memo[1][i] = 1
            else:
                memo[1][i]=0
    print()
    # Solving knapsack BACKWARDS
    f = f_backward(memo, c, A, b, n, j+1)

    print()
    print('After calculating memoization:')
    print()

    # write_table(memo)
    print("Memo:")
    for i in memo:
        print(i)
    
    reconstruct_backward(memo, n, j+1,A , c, solution)

    for i in range(len(tmp)):
        if tmp[i]!=0:
            solution.insert(i,tmp[i])
            A.insert(i,tmp_A[i])
            c.insert(i,pom_C[i])

    print()
    print('Optimal arrangement is: {}'.format(solution))

    f = sum(i*j for i,j in zip(solution, c) if i!=math.inf)


    print('Optimal value is: {} '.format(f),end='')
    if any(i == math.inf for i in solution):
        print('+ {}'.format(math.inf))
    
    print_split()

