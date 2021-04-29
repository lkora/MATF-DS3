from .print_ import print_simplex_table

decimal_space = 2

def dual_simplex(table,B):
    print()
    # We do dual simplex untill all variables become integers
    iteration = 0
    while not all(a[-1] >= 0 for a in table[:-1]):

        n_b = -1
        for i in range(len(table)-1):
            if table[i][-1] < 0:
                n_b = i
                break
        # Looking for pivoting index
        ind = find_pivot(table,B,n_b)
        print()
        print('Pivoting around the element A[{}][{}]: {}'.format(n_b,ind,round(table[n_b][ind],decimal_space)))
        old = table[n_b][ind]
        table[n_b] = [a/old for a in table[n_b]]

        for j in range(len(table)):
            if j!=n_b:
                mult = table[j][ind]
                table[j] = [a-mult*k for a,k in zip(table[j],table[n_b])]
        B[n_b] = ind
        print()
        print('After pivoting:')
        print('Iteration {}'.format(iteration))
        print('---------------')
        print_simplex_table(table, B, [], [])
        iteration += 1
    print()
    print("All b > 0, stop")
    return table, B


def find_pivot(table, B, nb):
    tmp = []
    ind = -1
    print('Candidates for lexicographical alignment: ')
    for i in range(len(table[nb])-1):
        if table[nb][i] < 0 and i not in B:

            row = [table[j][i] for j in range(len(table)-1) if j!=nb]
            row.insert(0, table[-1][i])
            f = table[nb][i]

            if round(f,decimal_space).is_integer():
                    print('{} / {}'.format([ int(round(a,decimal_space)) if round(a,decimal_space).is_integer() else round(a,decimal_space) for a in row ],
                    int(round(-table[nb][i],decimal_space))))
            else:
                    print('{} / {}'.format([ int(round(a,decimal_space)) if round(a,decimal_space).is_integer() else round(a,decimal_space) for a in row ],
                    round(-table[nb][i],decimal_space) ))

            tmp.append([a/(-f) for a in row])
        else :
            tmp.append(None)
        
    if all(i==None for i in tmp):
        print("No negative variables in the current row => no feasable solutions")
        quit()
    
    for i in range(len(tmp)):
        if tmp[i]!=None:
            ind = i
            break

    for i in range(len(tmp)):
        if tmp[i]!=None: 
            indexi = [j for j in range(len(tmp)) if j!=i and tmp[j]!=None]
            if all(tmp[i] < tmp[j] for j in indexi ):
                ind = i
                break

    return ind

