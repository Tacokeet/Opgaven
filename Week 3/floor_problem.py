import itertools

'''
Rule set Floor Puzzle:
L not (4e verdieping)
M not (Begane grond)
N not (Begane grond) and not (4e verdieping)
E at least 1 higher than M
J not neighbour of M

'''
for (L, M, N, E, J) in list(
        itertools.permutations([0, 1, 2, 3, 4])):
    if L is not 4:
        if M is not 0:
            if N is not 0 and N is not 4:
                if E < M:
                    if (J - M) > 2:
                        print("Loes woont op : " + str(L))
                        print("Marja woont op : " + str(M))
                        print("Niels woont op : " + str(N))
                        print("Erik woont op : " + str(E))
                        print("Joep woont op : " + str(J))
                        print("----------------------------------")

