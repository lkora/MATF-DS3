
def clean_from_artificial(table, B, W):
    while len(W):
        nonbase = [w for w in W if w not in B]
        for i in range(len(nonbase)):
            for j in range(len(table)):
                table[j].pop(nonbase[i])
            old = nonbase[i]
            nonbase = [n if n<old else n-1 for n in nonbase]

            W.remove(old)
            W = [w if w<old else w-1 for w in W]
            B = [w if w<old else w-1 for w in B]

        basis = [w for w in W if w in B]


        for b in basis:
            ind = B.index(b)

            if any(table[ind][i]!=0 for i in range(len(table[ind])-1) if i!=ind):
                candidates = [i for i in range(len(table[ind])-1) if i!=ind and table[ind][i]!=0]
                column = candidates[0]

                st = table[ind][column]
                table[ind] = [i/st for i in table[ind]]

                for i in range(len(table)):
                    if i!=ind:
                        mult = table[i][column]
                        table[i] = [j-mult*k for j,k in zip(table[i],table[ind])]
                B[ind] = column
            else:
                table.pop(ind)
                B.pop(ind)
                for i in range(len(table)):
                    table[i].pop(b)
                basis.remove(b)
                W.remove(b)
                basis = [n if n<b else n-1 for n in basis]
                W = [w if w<b else w-1 for w in W]
                B = [w if w<old else w-1 for w in B]
    return table, B


