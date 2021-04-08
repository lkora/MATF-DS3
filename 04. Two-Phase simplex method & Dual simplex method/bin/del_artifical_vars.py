import random
import math
import numpy as np

def del_artifical_vars(table, B, W):
    koristi_blenda = True
    pisi_korake = True
    while len(W)!=0:
        #brisemo vestacke promenljive tako sto radimo sledece:
        #ako nisu bazisne odmah ih samo precrtamo
        nebazisne = [i for i in W if i not in B]
        if pisi_korake:
            print()
            print('Tabela pre uklanjanja nebazisnih')
            for r in table:
                print([round(i, 2) for i in r])
            print()
            print('Uklanjamo vestacke koje su nebazisne')
            print('nebazisne vestacke = {}'.format(nebazisne))
        for i in range(len(table)):
            table[i] = [vrednost for index,vrednost in enumerate(table[i]) if index not in nebazisne ]
        #ovde azuriramo vestacke indekse ako smo uklonili neku koja je manja od w moramo da mu smanjimo indeks
        #da bi odgovarao dobijenoj tabeli
        W = [i for i in W if i not in nebazisne]
        for i in range(len(W)):
            br_manjih = len([j for j in nebazisne if j <W[i]])
            W[i] -=br_manjih

        for i in range(len(B)):
            br_manjih = len([j for j in nebazisne if j <B[i]])
            B[i] -=br_manjih

        if pisi_korake:
            print('Tabela nakon uklanjanja nebazisnih')
            for r in table:
                print([round(i, 2) for i in r])
            print()
            print('Uklanjamo vestacke koje su bazisne')
            print('bazisne vestacke = {}'.format(W))
        #sada uklanjamo vestacke koje su bazisne sve
        #ako su u jednom redu sve 0 osim 1 za tu bazisnu vestacku onda uklanjamo taj red i tu kolonu
        #inace ako postoji neki element koji je razlicit od 0 , uzmemo neki takav i napravimo ga bazisnim
        #nakon toga posto ta vestacka vise nije bazisna brise se isto kao malopre
        obrisane = []
        for w in W:
            # red = B.index(w)
            red = np.where(B == w)[0].item()
            indexi = [i for i,j in enumerate(table[red][:-1]) if i!=w]
            nenula = any(table[red][i]!=0 for i in indexi)

            if nenula:
                #ako postoji neki koji nije nula uzimamo neki od njih i pravimo ga bazom sa pivotiranjem
                kandidati = [i for i in indexi if table[red][i]!=0]
                ind = kandidati[0]
                if not koristi_blenda:
                    ind = random.choice(kandidati)

                table[red] = [i/table[red][ind] for i in table[red]]

                for i in range(len(table)):
                    if i!=red:
                        mult = -table[i][ind]
                        table[i] = [i+mult*j for i,j in zip(table[i],table[red])]
                B[red] = ind
                if pisi_korake:
                    print('Posto vestacka x{} u redu ima el!=0 pivotiramo oko A[{}][{}]'.format(w, red, ind))
                    print('Nova baza je {}'.format(B))
                    print()
            else:
                #ako je 0 sve onda brisemo red i kolonu
                table.pop(red)
                for i in range(len(table)):
                    table[i].pop(w)

                B = B.tolist()
                el = B.pop(red)
                # FIx this shit!
                B = [i if el>i else i-1 for i in B]
                W.remove(w)
                W = [i if el > i else i - 1 for i in W]
                B = np.array(B)
                if pisi_korake:
                    print('Posto vestacka x{} u redu gde je bazisna su sve 0 brisemo red i kolonu'.format(w))
            if pisi_korake:
                print()
                print('Tabela nakon uklanjanja bazisnih')
                for r in table:
                    print([round(i, 2) for i in r])

    return table,B
