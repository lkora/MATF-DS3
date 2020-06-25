import numpy as np
import copy
import math

#np.set_printoptions(suppress=False, precision=3)

class Cvor:

    def __init__(self, s):

        self.tabela = copy.deepcopy(s)  # Klasa sistem
        self.levo = None
        self.desno = None
        self.rez = self.tabela.rez_funkcije[0] * (-1) if self.tabela.problem == "min" else self.tabela.rez_funkcije[0]
        self.optimalno = self.nadji_opt()

    def nadji_opt(self):

        tab = self.tabela
        opt_resenje = np.zeros(tab.br_kolona)

        for i in range(tab.br_kolona):

            jedinice = np.where(tab.matricaA[:, i] == 1)[0]
            nule = np.where(tab.matricaA[:, i] == 0)[0]

            if len(jedinice) == 1 and len(nule) == tab.br_vrsta - 1:
                opt_resenje[i] = tab.matricaB[jedinice[0]]

        return opt_resenje[:gl_kolone]

    def dodaj_levo_desno(self, indeks, vr):

        l = math.floor(vr)
        d = l + 1
        print("vrednosti po kojim granamo l i d:", l, d)

        # Dodaj ogranicenje za levi kraj
        tab_l = copy.deepcopy(self.tabela)
        tab_l.matricaA = np.append(tab_l.matricaA, np.zeros((tab_l.br_vrsta, 1)), axis=1)
        tab_l.br_kolona += 1
        linija = np.zeros(tab_l.br_kolona)
        linija[indeks] = 1
        linija[-1] = 1
        tab_l.matricaA = np.append(tab_l.matricaA, [linija], axis=0)
        tab_l.matricaB = np.append(tab_l.matricaB, [[l]], axis=0)
        tab_l.koefs_problema = np.append(tab_l.koefs_problema, 0)
        tab_l.br_vrsta += 1
        tab_l.niz_znakova = np.append(tab_l.niz_znakova, "=")
        print(tab_l.niz_znakova)

        ispis(tab_l)

        # Dodaj ogranicenje za desni kraj
        tab_d = copy.deepcopy(self.tabela)
        tab_d.matricaA = np.append(tab_d.matricaA, np.zeros((tab_d.br_vrsta, 1)), axis=1)
        tab_d.br_kolona += 1
        linija = np.zeros(tab_d.br_kolona)
        linija[indeks] = -1
        linija[-1] = 1
        tab_d.matricaA = np.append(tab_d.matricaA, [linija], axis=0)
        tab_d.matricaB = np.append(tab_d.matricaB, [[-d]], axis=0)
        tab_d.koefs_problema = np.append(tab_d.koefs_problema, 0)
        tab_d.br_vrsta += 1
        tab_d.niz_znakova = np.append(tab_d.niz_znakova, "=")
        ispis(tab_d)

        print("Trazimo resenja za levi i desni cvor:")
        jedn_ili_vece = np.copy(tab_l.niz_znakova)
        tab_l = odg_simpleks(tab_l, jedn_ili_vece)
        print("levi kraj")
        ispis(tab_l)

        jedn_ili_vece = np.copy(tab_d.niz_znakova)
        tab_d = odg_simpleks(tab_d, jedn_ili_vece)
        print("desni kraj")
        ispis(tab_d)

        baz_cel_l, baz_cel_d = None, None

        if tab_l is not None:
            self.levo = Cvor(tab_l)
            baz_cel_l = bazisne_celobrojne(self.levo.tabela)
        else:
            self.levo = None

        if tab_d is not None:
            self.desno = Cvor(tab_d)
            baz_cel_d = bazisne_celobrojne(self.desno.tabela)
        else:
            self.desno = None

        print("bazisne celobrojne:", baz_cel_l, baz_cel_d)
        return self.levo, self.desno


class Sistem:

    def __init__(self):

        self.br_vrsta = 0
        self.br_kolona = 0
        self.rez_funkcije = np.array([0])  # rezultat funkcije!
        self.problem = ""
        self.koefs_problema = np.array([])
        self.niz_znakova = np.array([])
        self.matricaA = np.array([])
        self.matricaB = np.array([])
        self.P = np.array([])
        self.Q = np.array([])
        self.x = np.array([])

        self.baz_prom = 0

blend = "da"
gl_vrste = 0
gl_kolone = 0

# Funkcija za unos
def unesiUlaz(s):
    global blend, gl_vrste, gl_kolone
    funkcija = input("Unesite problem ( u obliku max ili min) i koeficijente funkcije:").split(" ")

    if funkcija[0] == "max" or funkcija[0] == "min":
        s.problem = str(funkcija[0])
    else:
        print("\n Pogresan unos problema.")
        exit()

    s.koefs_problema = np.array(list(map(float, funkcija[1:])))

    ulaz = input("Unesite broj nejednacina i broj nepoznatih, NE racunajuci podrazumevane x1>=0...):")

    s.br_vrsta = int(ulaz.split(" ")[0])
    s.br_kolona = int(ulaz.split(" ")[1])
    gl_vrste = s.br_vrsta
    gl_kolone = s.br_kolona

    s.baz_prom = int(ulaz.split(" ")[1])

    s.matricaA = np.zeros((s.br_vrsta, s.br_kolona))
    s.matricaB = np.zeros((s.br_vrsta, 1))

    for i in range(s.br_vrsta):

        linija = input("Unesite sve koeficijente nejednacine kao i znak:").split(" ")
        s.niz_znakova = np.append(s.niz_znakova, linija[-2])
        koefs_nejednacine = list(map(float, linija[:-2] + linija[-1:]))
        duzina = len(koefs_nejednacine)

        for j in range(duzina):
            if j == duzina - 1:
                s.matricaB[i][0] = koefs_nejednacine[j]
            else:
                s.matricaA[i][j] = koefs_nejednacine[j]

    blend = input("Unesite da/ne za koriscenje Blendovog pravila")
    print("niz znakova", len(s.niz_znakova))


# Funkcija za svodjenje na kanonski oblik
def kanonskiOblik(s):
    j = s.br_kolona

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        # s.problem = "min"
        s.koefs_problema *= (-1)

    for i in range(s.br_kolona):
        s.Q = np.append(s.Q, i)

    # Prebacujemo nejednacine u jednacine
    for i in range(s.br_vrsta):

        if s.niz_znakova[i] != "=":

            nule = np.zeros((s.br_vrsta, 1))

            if s.niz_znakova[i] == ">=":
                nule[i][0] = -1
            elif s.niz_znakova[i] == "<=":
                nule[i][0] = 1

            s.matricaA = np.append(s.matricaA, nule, axis=1)
            s.niz_znakova[i] = "="
            s.br_kolona += 1  # Izmenjen broj kolona
            if nule[i][0] == 1:
                s.P = np.append(s.P, j)
            elif nule[i][0] == -1:
                s.Q = np.append(s.Q, j)
            j += 1

    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    s.koefs_problema = np.append(s.koefs_problema, np.zeros((1, s.br_kolona - len(s.koefs_problema))))


# Pomocna funkcija za proveru uslova
def proveriUslov(koefs):
    for i in range(len(koefs)):
        if koefs[i] < 0:
            return False

    return True


# Pomocna funkcija za pronalazenje indeksa
def pronadjiIndeks(koefs, s):
    for i in range(len(koefs)):
        if koefs[i] < 0:
            return s.Q[i]


def ispis(s2):

    if s2 == None:
        print("Nemoguc ispis, nepostojeca matrica")
        return

    mat = s2.matricaA
    mat2 = s2.matricaB

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            print('{: 3.3f}'.format(mat[i][j]), end=" ")
        print('{: 3.3f}'.format(mat2[i][0]))

    for i in range(len(s2.koefs_problema)):
        print('{: 3.3f}'.format(s2.koefs_problema[i]), end=" ")
    print(s2.rez_funkcije)

    print("-----------------")


# Pomocna funkcija za obavljanje elementarnih transfomacija nad matricom
def elem_transformacije(s2, pivot_vrsta, pivot_kolona, pivot_vrednost):
    for k in range(s2.br_vrsta):

        if k != pivot_vrsta:
            stara_pivot_kolona = s2.matricaA[k][pivot_kolona]
            s2.matricaA[k] = s2.matricaA[k] + (-1) * stara_pivot_kolona / pivot_vrednost * s2.matricaA[
                pivot_vrsta]
            s2.matricaB[k] = s2.matricaB[k] + (-1) * stara_pivot_kolona / pivot_vrednost * s2.matricaB[
                pivot_vrsta]

        stara_pivot_kolona_c = s2.koefs_problema[pivot_kolona]
        s2.koefs_problema = s2.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s2.matricaA[
            pivot_vrsta]
        s2.rez_funkcije = s2.rez_funkcije + (-1) * stara_pivot_kolona_c / pivot_vrednost * s2.matricaB[
            pivot_vrsta]

        # Ako je decimalni deo manji od 0.01 zaokruzujemo na ceo broj
        zaokruzi(s2)

    # Delimo celu vrstu sa trenutnim pivotom
    if pivot_vrednost != 0:
        s2.matricaA[pivot_vrsta] = s2.matricaA[pivot_vrsta] / pivot_vrednost
        s2.matricaB[pivot_vrsta] = s2.matricaB[pivot_vrsta] / pivot_vrednost

        zaokruzi(s2)


# Pomocna funkcija za transformisanje koeficijenata ispod bazisnih kolona
def ciscenje_koefs_problema(s3):
    for i in range(s3.br_kolona):

        jedinice = np.where(s3.matricaA[:, i] == 1)[0]
        nule = np.where(s3.matricaA[:, i] == 0)[0]

        if len(jedinice) == 1 and len(nule) == s3.br_vrsta - 1:

            stari_koef = s3.koefs_problema[i]
            if stari_koef != 0:
                indeks_1 = jedinice[0]
                s3.koefs_problema = s3.koefs_problema + (-1) * stari_koef * s3.matricaA[indeks_1, :]
                s3.rez_funkcije = s3.rez_funkcije + (-1) * stari_koef * s3.matricaB[indeks_1, :]

        ispis(s3)


def tablicni_simpleks(s):
    iteracija = 1

    while iteracija < 300:
        print("Iteracija:", iteracija)

        for k in range(len(s.koefs_problema)):

            if s.koefs_problema[k] < 0:

                # Provera da li su svi iznad c negativni; ako je T -> neogranicen problem
                br_negativnih = 0
                for m in range(s.br_vrsta):
                    if s.matricaA[m][k] >= 0:
                        break
                    else:
                        br_negativnih += 1

                if br_negativnih == s.br_vrsta:
                    print("Neogranicen problem")
                    s.rez_funkcije[0] = float('-inf')
                    return
                    #exit()

                # Trazimo pivot
                min = 100
                pivot_vrsta = 30
                pivot_kolona = 30
                pivot_vrednost = 30
                for i in range(s.br_vrsta):
                    if s.matricaA[i][k] > 0:
                        nova_vr = s.matricaB[i][0] / s.matricaA[i][k]

                        # Trenutni min
                        if blend == "da":
                            if min > nova_vr:  # Koriscenjem Blendovog pravila
                                min = nova_vr
                                pivot_vrsta = i
                                pivot_kolona = k
                                pivot_vrednost = s.matricaA[i][k]
                        else:
                            if min >= nova_vr:  # Bez koriscenja pravila
                                min = nova_vr
                                pivot_vrsta = i
                                pivot_kolona = k
                                pivot_vrednost = s.matricaA[i][k]

                elem_transformacije(s, pivot_vrsta, pivot_kolona, pivot_vrednost)
                break

        ispis(s)

        # Proveravamo da li su svi c-ovi nenegativni; ako T -> nasli smo optimalno resenje
        br_pozitivnih = 0
        for i in range(len(s.koefs_problema)):
            if s.koefs_problema[i] >= 0:
                br_pozitivnih += 1

        # Ispisujemo optimalno i vrednost funkcije
        if br_pozitivnih == len(s.koefs_problema):

            # pronalazenje optimalnog resenja
            opt_resenje = np.zeros(s.br_kolona)
            for i in range(s.br_kolona):

                jedinice = np.where(s.matricaA[:, i] == 1)[0]
                nule = np.where(s.matricaA[:, i] == 0)[0]

                if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1:
                    opt_resenje[i] = s.matricaB[jedinice[0]]

            print("\nKorisceno Blendovo pravilo:", blend)

            if np.size(np.where(opt_resenje[:s.baz_prom] < 0)[0]) > 0:
                print("Nema dopustivih tacaka", opt_resenje[:s.baz_prom])
                s.rez_funkcije[0] = float('-inf')
                return
                #exit()

            if s.problem == "min":
                print("min f:", s.rez_funkcije[0] * (-1))
            else:
                print("max f:", s.rez_funkcije[0])

            print("Optimalno resenje:\n", end="")
            for i in range(len(opt_resenje)):
                print('{: 3.3f}'.format(opt_resenje[i]), end=" ")
            print("")
            return s

        iteracija += 1


def dualni_simpleks(s):
    iteracija = 1

    while iteracija < 100:
        print("Iteracija:", iteracija)

        for k in range(len(s.matricaB)):
            if s.matricaB[k] < 0:

                # Provera da li su svi a-ovi pozitivni; ako T -> neogranicen problem
                br_poz = 0
                for m in range(s.br_kolona):
                    if s.matricaA[k][m] < 0:
                        break
                    else:
                        br_poz += 1

                if br_poz == s.br_kolona:
                    print("Neogranicen problem")
                    s.rez_funkcije[0] = float('-inf')
                    return
                    #exit()

                # Trazimo pivot
                max = -100
                pivot_vrsta = 30
                pivot_kolona = 30
                pivot_vrednost = 30

                for i in range(s.br_kolona):
                    if s.matricaA[k][i] < 0:
                        nova_vr = s.koefs_problema[i] / s.matricaA[k][i]

                        # Trenutni max
                        if blend == "da":
                            if max < nova_vr:  # Koriscenjem Blendovog pravila
                                max = nova_vr
                                pivot_vrsta = k
                                pivot_kolona = i
                                pivot_vrednost = s.matricaA[k][i]

                        else:
                            if max <= nova_vr:  # Bez koriscenje pravila
                                max = nova_vr
                                pivot_vrsta = k
                                pivot_kolona = i
                                pivot_vrednost = s.matricaA[k][i]

                print("Pivot (vrsta, kolona, vrednost):", pivot_vrsta, pivot_kolona, pivot_vrednost, "\n")

                # Obavljamo elementarne transformacije nad ostalim vrstama - vrsimo pivotiranje
                for i in range(s.br_vrsta):

                    if i != pivot_vrsta:
                        stara_pivot_kolona = s.matricaA[i][pivot_kolona]
                        s.matricaA[i] = s.matricaA[i] + (-1) * stara_pivot_kolona / pivot_vrednost * s.matricaA[
                            pivot_vrsta]
                        s.matricaB[i] = s.matricaB[i] + (-1) * stara_pivot_kolona / pivot_vrednost * s.matricaB[
                            pivot_vrsta]

                    stara_pivot_kolona_c = s.koefs_problema[pivot_kolona]
                    s.koefs_problema = s.koefs_problema + (-1) * stara_pivot_kolona_c / pivot_vrednost * s.matricaA[
                        pivot_vrsta]
                    s.rez_funkcije = s.rez_funkcije + (-1) * stara_pivot_kolona_c / pivot_vrednost * s.matricaB[
                        pivot_vrsta]

                    # Zaokruzujemo sve vrednosti na dve decimale
                    zaokruzi(s)

                # Delimo celu vrstu sa trenutnim pivotom
                if pivot_vrednost != 0:
                    s.matricaA[pivot_vrsta] = s.matricaA[pivot_vrsta] / pivot_vrednost
                    s.matricaB[pivot_vrsta] = s.matricaB[pivot_vrsta] / pivot_vrednost

                    zaokruzi(s)

                break

        ispis(s)

        # Proveravamo da li su svi b-ovi nenegativni; ako T -> nasli smo optimalno resenje
        br_pozitivnih = 0

        for i in range(len(s.matricaB)):
            if s.matricaB[i] >= 0:
                br_pozitivnih += 1

        # Ispisujemo optimalno i vrednost funkcije
        if br_pozitivnih == len(s.matricaB):

            # Pronalazenje optimalnog resenja
            opt_resenje = np.zeros(s.br_kolona)
            for i in range(s.br_kolona):

                jedinice = np.where(s.matricaA[:, i] == 1)[0]
                nule = np.where(s.matricaA[:, i] == 0)[0]

                if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1:
                    opt_resenje[i] = s.matricaB[jedinice[0]]

            print("\nKorisceno Blendovo pravilo:", blend)

            # Ako je neko od resenja negativno
            if np.size(np.where(opt_resenje[:s.baz_prom] < 0)[0]) > 0:
                print("Nema dopustivih tacaka", opt_resenje[:s.baz_prom])
                s.rez_funkcije[0] = float('-inf')
                return
                #exit()

            if s.problem == "min":
                print("min f:", s.rez_funkcije[0] * (-1))
            else:
                print("max f:", s.rez_funkcije[0])

            print("Optimalno resenje:\n", end="")
            for i in range(len(opt_resenje)):
                print('{: 3.3f}'.format(opt_resenje[i]), end=" ")
            print("")
            return s

        iteracija += 1


# Pomocna fja za proveru postojanja negativnih c-ova
def negativni_c(s):

    c_ovi = s.koefs_problema
    for c in c_ovi:
        if c < 0:
            return True

    return False


# Pomocna fja za proveru postojanja negativnih b-ova
def negativni_b(s):

    b_ovi = s.matricaB
    for b in b_ovi:
        if b[0] < 0:
            return True

    return False


# Ako je decimalni deo manji od 0.01 zaokruzujemo na ceo broj
def zaokruzi(s):

    for i, lin in enumerate(s.matricaA):
        for j, vr in enumerate(lin):
            s.matricaA[i][j] = round(vr, 3) + 0
            # if abs(vr) % 1 < 0.01:
            #     s.matricaA[i][j] = round(vr, 1)

    for i, vr in enumerate(s.matricaB):
        s.matricaB[i][0] = round(vr[0], 3) + 0
        # if abs(vr[0]) % 1 < 0.01:
        #     s.matricaB[i][0] = round(vr[0], 1)

    for i, vr in enumerate(s.koefs_problema):
        s.koefs_problema[i] = round(vr, 3) + 0
        # if abs(vr) % 1 < 0.01:
        #     s.koefs_problema[i] = round(vr, 1)

    s.rez_funkcije = np.round(s.rez_funkcije, 3) + 0
    #s.rez_funkcije[abs(s.rez_funkcije) % 1 < 0.01] = np.round(s.rez_funkcije, 1)
    return s


# Pomocna fja za proveru postojanja pocetne baze
def postoji_baza(s):

    bazisne_kol = 0

    for i, vr in enumerate(s.matricaA.T):
        jedinice = np.where(vr == 1)[0]
        nule = np.where(vr == 0)[0]
        if len(jedinice) == 1 and len(nule) == s.br_vrsta - 1 and s.koefs_problema[i] == 0:
            bazisne_kol += 1

    if bazisne_kol == s.br_vrsta:
        return True
    else:
        return False


# Funkcija za proveru celobrojnosti resenja x1,x2...
def bazisne_celobrojne(s3):

    sve_jed = np.zeros(s3.baz_prom)
    for t in range(s3.baz_prom):

        jedinice = np.where(s3.matricaA[:, t] == 1)[0]
        nule = np.where(s3.matricaA[:, t] == 0)[0]
        if len(jedinice) == 1 and len(nule) == s3.br_vrsta - 1:
            sve_jed[t] = jedinice

    for k, i in enumerate(sve_jed):
        if s3.matricaB[int(i)] % 1 != 0:
            return False, k, s3.matricaB[int(i)]

    return True, -1, -1


def odg_simpleks(s, jedn_ili_vece):
    ispis(s)
    #Pozivamo odgovarajuci Simpleks
    if negativni_b(s) and postoji_baza(s):

        print("B ima negativnih pozivamo dualni simpleks\n")
        s = dualni_simpleks(s)
        return s

    elif negativni_c(s) and postoji_baza(s):

        print("C ima negativnih pozivamo tablicni simpleks\n")
        s = tablicni_simpleks(s)
        return s

    else:  # nema pocetne baze
        s = dvofazni_simpleks(s, jedn_ili_vece)
        return s


def dvofazni_simpleks(s, jedn_ili_vece):

    print("\n######################Prva faza:######################\n")
    s2 = Sistem()
    s2 = copy.deepcopy(s)
    s2.koefs_problema = np.zeros((len(s.koefs_problema)))

    s2.rez_funkcije[0] = 0

    # Ako je neko b < 0 mnozimo celu vrstu sa -1
    for p, l in enumerate(s2.matricaB):
        if l[0] < 0:
            s2.matricaA[p][s2.matricaA[p] != 0] *= -1
            s2.matricaB[p][0] *= -1

    for i in range(len(jedn_ili_vece)):
        if jedn_ili_vece[i] == ">=" or jedn_ili_vece[i] == "=":
            dodatni = np.zeros((s.br_vrsta, 1))
            dodatni[i] = 1
            s2.matricaA = np.append(s2.matricaA, dodatni, axis=1)
            s2.br_kolona += 1
            s2.koefs_problema = np.append(s2.koefs_problema, 1)
            s2.P = np.append(s2.P, s2.br_kolona - 1)

    s2.P = np.array(list(map(int, s2.P)))

    vestacke = np.where(s2.koefs_problema == 1)[0]

    ispis(s2)

    # Vrsimo elementarne transformacije kako bi dobili bazisne kolone
    ciscenje_koefs_problema(s2)

    ispis(s2)
    print("Trenutna vrednost funkcije:", s2.rez_funkcije[0])

    print("Pozivamo tablicni simplex u prvoj fazi:")
    tablicni_simpleks(s2)

    if s2.rez_funkcije[0] != 0:
        print("\n Rezultat pomocnog problema:", s2.rez_funkcije[0],
              "!= 0 => pocetni problem nema dopustivih resenja. STOP")
        s2.rez_funkcije[0] = float('-inf')
        return
        #exit()

    # Brisanje vestackih promenljivih
    pom = np.array([])
    for i in vestacke:
        if (len(np.where(s2.matricaA[:, i] == 1)[0]) != 1 or \
                len(np.where(s2.matricaA[:, i] == 0)[0]) != s2.br_vrsta - 1) or s2.koefs_problema[i] != 0:
            s2.matricaA[:, i] = np.zeros(s2.br_vrsta)
            s2.koefs_problema[i] = 0
            pom = np.append(pom, i)
            vestacke = np.delete(vestacke, np.where(vestacke == i))

    # Prolazimo preostale vestacke bazisne kolone i brisemo odgovarajucu vrstu ako su sve nule u vrsti ili
    # nalazimo pivot i obavljamo transformacije
    for i in vestacke:

        jedinice = np.where(s2.matricaA[:, i] == 1)[0]
        nule = np.where(s2.matricaA[:, i] == 0)[0]

        if len(jedinice) == 1 and len(nule) == s2.br_vrsta - 1:

            indeks_vr = jedinice[0]
            ne_nule = np.where(s2.matricaA[indeks_vr, :] != 0)[0]

            # Ako su sve nule u vrsti osim jedinice koja pripada bazisnoj koloni -> brisemo vrstu
            if len(ne_nule) == 1 and ne_nule[0] == i:

                s2.matricaA = np.delete(s2.matricaA, indeks_vr, axis=0)
                s2.br_vrsta -= 1

            # Nasli smo ne nula vrednost u vrsti, uzimamo za pivot i obavljamo elem. transformacije
            else:

                # novi pivot je prvi != 0 u toj vrsti
                if ne_nule[0] != i:  # da ne uzmemo bas tog jedinog keca

                    pivot_vrsta = indeks_vr
                    pivot_kolona = ne_nule[0]
                    pivot_vrednost = s2.matricaA[pivot_vrsta][pivot_kolona]

                    elem_transformacije(s2, pivot_vrsta, pivot_kolona, pivot_vrednost)

    # Brisemo sve vestacke kolone
    pom = np.append(pom, vestacke)
    s2.matricaA = np.delete(s2.matricaA, pom, axis=1)
    s2.koefs_problema = np.delete(s2.koefs_problema, pom, axis=0)
    s2.br_kolona -= len(pom)

    print("\n######################Druga faza:######################\n")

    s3 = copy.deepcopy(s2)
    s3.koefs_problema = s.koefs_problema
    s3.br_kolona = len(s3.matricaA[0])
    s3.br_vrsta = len(s3.matricaA)

    s3.rez_funkcije[0] = s.rez_funkcije[0]


    ciscenje_koefs_problema(s3)

    tablicni_simpleks(s3)
    s = copy.deepcopy(s3)
    return s



def main():
    s = Sistem()
    unesiUlaz(s)
    jedn_ili_vece = np.copy(s.niz_znakova)

    print("Ulaz:\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.niz_znakova)
    ispis(s)

    # Ako je bila nejednacina oblika >= hocemo <=
    for i in range(s.br_vrsta):
        if s.niz_znakova[i] == ">=":
            s.matricaB[i] *= -1
            s.matricaA[i] *= -1
            s.niz_znakova[i] = "<="

    kanonskiOblik(s)
    print("U kanonskom obliku:\n", s.br_vrsta,
          s.br_kolona,
          s.rez_funkcije,
          s.problem,
          s.niz_znakova)
    ispis(s)

    s = odg_simpleks(s, jedn_ili_vece)

    koren = Cvor(s)
    baz_cel = bazisne_celobrojne(s)
    if baz_cel[0]:
        print("Koren vec ima celobrojna resenja")
        exit()

    a, b = koren.dodaj_levo_desno(baz_cel[1], baz_cel[2][0])

    M = float('+inf')
    opt = None

    while 1:

        b_a, b_b = None, None
        if a is not None:
            b_a = bazisne_celobrojne(a.tabela)
        if b is not None:
            b_b = bazisne_celobrojne(b.tabela)
        print(b_a, b_b)

        # Ako imamo celobrojno resenje proveravamo da li je bolje od rekorda
        if b_a is not None and b_a[0] and round(a.rez, 1) < M:
            M = round(a.rez, 1)
            opt = a.optimalno

        if b_b is not None and b_b[0] and round(b.rez, 1) < M:
            M = round(b.rez, 1)
            opt = b.optimalno
        print("Rekord:", M, opt)

        print("Tekuci uslovi:", b_a, b_b)
        if b_a is None:
            if b_b is None or b_b[0]:
                exit()
            else:
                a, b = b.dodaj_levo_desno(b_b[1], b_b[2][0])

        elif b_b is None:
            if b_a is None or b_a[0]:
                exit()
            else:
                a, b = a.dodaj_levo_desno(b_a[1], b_a[2][0])

        elif b_a[0] and b_b[0]:
            exit()

        elif not b_a[0] and not b_b[0]:
            if a.rez < b.rez:
                a, b = a.dodaj_levo_desno(b_a[1], b_a[2][0])
            else:
                a, b = b.dodaj_levo_desno(b_b[1], b_b[2][0])

        elif b_a[0] and not b_b[0]:
            a, b = b.dodaj_levo_desno(b_b[1], b_b[2][0])

        elif not b_a[0] and b_b[0]:
            a, b = a.dodaj_levo_desno(b_a[1], b_a[2][0])

        else:
            exit()


if __name__ == '__main__':
    main()
