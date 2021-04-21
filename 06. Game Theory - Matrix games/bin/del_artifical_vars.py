import random
import math
import numpy as np

def del_artifical_vars(table, B, W, print_steps=False, use_bland=True):
    
    while len(W)!=0:
        # Removing aritficial variables:
        # If they are not in the base we cross them over
        non_basis = [i for i in W if i not in B]
        if print_steps:
            print()
            print('Table before removing base variables')
            for r in table:
                print([round(i, 2) for i in r])
            print()
            print('Removing aritificial, non basis, vars')
            print('non_basis = {}'.format(non_basis))
        for i in range(len(table)):
            table[i] = [value for index,value in enumerate(table[i]) if index not in non_basis ]
        # Uprading artifiicial var indexes
        # If we removed any variable that was smaller than w we have to remove it's index too so that
        # it can correspond to the table W
        W = [i for i in W if i not in non_basis]
        for i in range(len(W)):
            smaller_num = len([j for j in non_basis if j <W[i]])
            W[i] -=smaller_num

        for i in range(len(B)):
            smaller_num = len([j for j in non_basis if j <B[i]])
            B[i] -=smaller_num

        if print_steps:
            print('Table after removing non base variables')
            for r in table:
                print([round(i, 2) for i in r])
            print()
            print('Removing artificial base variables')
            print('Artificial base variables = {}'.format(W))
        # Removing all artificial base variables
        # If all are 0 in one row except 1, then we remove that artificial variable and we remove both the row
        # and the corresponding column 
        # Else if such an element exists that is different that 0, we choose it and make base
        # after that, since that artificial variable is no longer in base we remove it just like before
        removed = []
        for w in W:
            # row = B.index(w)
            row = np.where(B == w)[0].item()
            indexes = [i for i,j in enumerate(table[row][:-1]) if i!=w]
            nonzero = any(table[row][i]!=0 for i in indexes)

            if nonzero:
                # If there is an element that is not 0 we take any of them and make it a base by pivoting
                candidate = [i for i in indexes if table[row][i]!=0]
                ind = candidate[0]
                if not use_bland:
                    ind = random.choice(candidate)

                table[row] = [i/table[row][ind] for i in table[row]]

                for i in range(len(table)):
                    if i!=row:
                        mult = -table[i][ind]
                        table[i] = [i+mult*j for i,j in zip(table[i],table[row])]
                B[row] = ind
                if print_steps:
                    print('Since artificial variable x{} has an el!=0 in the same row, we pivot around A[{}][{}]'.format(w, row, ind))

                    print('New base is: {}'.format(B))
                    print()
            else:
                # If all are 0 then we delte both the row and the column
                table.pop(row)
                for i in range(len(table)):
                    table[i].pop(w)

                B = B.tolist()
                el = B.pop(row)

                B = [i if el>i else i-1 for i in B]
                W.remove(w)
                W = [i if el > i else i - 1 for i in W]
                B = np.array(B)
                if print_steps:
                    print('Since artificial variable x{} is in a row where the base is and all are = 0 we delete the row and the column'.format(w))
            if print_steps:
                print()
                print('Table after removing base variables')
                for r in table:
                    print([round(i, 2) for i in r])

    return table,B
