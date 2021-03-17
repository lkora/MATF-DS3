import numpy as np

# Funkcija za svodjenje na kanonski oblik
def make_canonical_form(s):
    j = s.br_kolona

    # Prebacujemo u problem nalazenja minimuma
    if s.problem == "max":
        s.problem = "min"
        s.koefs_problema *= (-1)

    for i in range(s.br_kolona):
        s.Q = np.append(s.Q, i)

    # Transforming inequations to equations, and b >= 0
    for i in range(s.br_vrsta):
        if s.niz_znakova[i] != "=":
            zeroes = np.zeros((s.br_vrsta, 1))
            if s.niz_znakova[i] == ">=":
                s.matricaB[i] *= -1
                s.matricaA[i] *= 1
                zeroes[i][0] = -1
            elif s.niz_znakova[i] == "<=":
                zeroes[i][0] = 1

            s.matricaA = np.append(s.matricaA, zeroes, axis=1)

            
            s.niz_znakova[i] = "="
            s.br_kolona += 1          # Changed number of columns
            s.P = np.append(s.P, j)
            j += 1

    s.Q = np.array(list(map(int, s.Q)))
    s.P = np.array(list(map(int, s.P)))
    s.koefs_problema = np.append(s.koefs_problema, np.zeros((1, len(s.P))))
