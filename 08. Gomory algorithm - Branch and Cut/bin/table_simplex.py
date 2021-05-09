import math

from .print_ import print_simplex_table

def table_simplex(table, B, S, W):
    print('Starting table simplex:')
    print()
    print_simplex_table(table, B, S, W)
    print()
    if any(i!=0 for i in table[-1][:-1]):
            print("Cleaning the function from basis variables")
            for b in B:
                if table[-1][b]!=0:
                    mult = table[-1][b]
                    ind = B.index(b)
                    table[-1] = [i-mult*j for i,j in zip(table[-1],table[ind])]

            print_simplex_table(table, B,S,W)

    iteration = 0

    while any(i<0 for i in table[-1][:-1]):
        print()
        print('Iteration : {}'.format(iteration))
        iteration += 1
        print('------------------------')

        candidates = [i for i,j in enumerate(table[-1][:-1]) if j<0 and i not in B]
        column = candidates[0]
        candidates = [ table[i][-1]/table[i][column] if table[i][column]>0 else math.inf for i in range(len(table[:-1]))]

        if all(i == math.inf for i in candidates):
            print('Upper bounded => No solution!')
            return None , B

        ind = candidates.index(min(candidates))

        print()
        print('Pivoting around the element A[{}][{}]'.format(ind,column))
        old = table[ind][column]
        table[ind] = [i/old for i in table[ind]]

        for i in range(len(table)):
            if i!=ind:
                mult = table[i][column]
                table[i] = [ j-mult*k for j,k in zip(table[i],table[ind])  ]

        B[ind] = column
        print_simplex_table(table, B, S, W)
        print()
    
    return table, B