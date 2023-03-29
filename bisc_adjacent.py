from permuta import *
from permuta.bisc import *


def min_index(L):
    mi = 0
    for i in range(len(L)):
        if L[i] < L[mi]:
            mi = i
    return mi


def fix_cycle(L):
    mi = min_index(L)
    return L[mi:] + L[:mi]


def Foata(perm):
    """
    given a permutation perm, outputs the image under Foata's fundamental bijection
    """
    cd = perm.cycle_decomp()
    cd = sorted(map(fix_cycle, cd), reverse=True)
    return Perm(tuple(sum(cd, [])))


def inverse_Foata(perm):
    """
    given a permutation perm, outputs the preimage under Foata's fundamental bijection
    """
    if len(perm) == 0:
        return perm
    ltrmins = list(perm.ltrmin())
    seqs = []
    for i in range(len(ltrmins) - 1):
        seqs.append(list(perm)[ltrmins[i] : ltrmins[i + 1]])
    seqs.append(list(perm)[ltrmins[-1] :])
    new_perm = [0] * len(perm)
    for i in range(len(seqs)):
        seq = seqs[i]
        if len(seq) == 1:
            new_perm[seq[0]] = seq[0]
        else:
            for j in range(len(seq)):
                new_perm[seq[j]] = seq[(j + 1) % len(seq)]
    return Perm(tuple(new_perm))


# p = Perm((2, 4, 3, 0, 1))
# p = Perm((0,))
# print(p)
# print(Foata(p))
# print(inverse_Foata(p))
# print(Foata(inverse_Foata(p)) == p)
# print(inverse_Foata(Foata(p)) == p)


def cycle_is_increasing(c):
    fc = fix_cycle(c)
    for j in range(len(fc) - 1):
        if fc[j + 1] - fc[j] != 1:
            return False
    return True


def has_increasing_cycle(perm, i):
    cd = perm.cycle_decomp()
    for c in cd:
        if len(c) == i:
            if cycle_is_increasing(c):
                return True
    return False


def num_increasing_cycles(perm, i):
    cd = perm.cycle_decomp()
    count = 0
    for c in cd:
        if len(c) == i:
            if cycle_is_increasing(c):
                count += 1
    return count


def cycle_is_sorted_increasing(c):
    fc = sorted(fix_cycle(c))
    for j in range(len(fc) - 1):
        if fc[j + 1] - fc[j] != 1:
            return False
    return True


def has_increasing_sorted_cycle(perm, i):
    cd = perm.cycle_decomp()
    for c in cd:
        if len(c) == i:
            if cycle_is_sorted_increasing(c):
                return True
    return False


q = 4
# auto_bisc(lambda perm: not has_increasing_cycle(inverse_Foata(perm), q))
# auto_bisc(lambda perm: not has_increasing_sorted_cycle(inverse_Foata(perm), q))

D = {
    4: {
        Perm((0, 1, 2, 3)): [
            {
                (0, 1),
                (2, 4),
                (1, 2),
                (3, 4),
                (2, 1),
                (4, 3),
                (3, 1),
                (0, 2),
                (2, 2),
                (1, 0),
                (3, 2),
                (1, 3),
                (4, 1),
                (4, 4),
                (0, 0),
                (1, 1),
                (0, 3),
                (2, 0),
                (4, 2),
                (1, 4),
                (2, 3),
                (3, 0),
                (3, 3),
                (4, 0),  # added
            }
        ]
    },
    5: {
        Perm((1, 2, 3, 4, 0)): [
            {
                (0, 1),
                (2, 4),
                (1, 2),
                (0, 4),
                (3, 4),
                (2, 1),
                (4, 3),
                (1, 5),
                (3, 1),
                (5, 4),
                (0, 2),
                (2, 2),
                (1, 0),
                (3, 2),
                (2, 5),
                (1, 3),
                (3, 5),
                (5, 2),
                (4, 4),
                (0, 0),
                (1, 1),
                (0, 3),
                (2, 0),
                (4, 2),
                (1, 4),
                (2, 3),
                (3, 0),
                (4, 5),
                (3, 3),
                (5, 3),
                (4, 1),  # added
                (4, 0),  # added
            }
        ]
    },
}
clpatt1 = list(D[4].keys())[0]
mesh1 = D[4][clpatt1][0]
clpatt2 = list(D[5].keys())[0]
mesh2 = D[5][clpatt2][0]

mp1 = MeshPatt(clpatt1, mesh1)
mp2 = MeshPatt(clpatt2, mesh2)

print(mp1.ascii_plot())
print("------------------")
print(mp2.ascii_plot())

for i in range(1, 10):
    for perm in Perm.of_length(i):
        numic = num_increasing_cycles(perm, q)
        Foata_of_perm = Foata(perm)
        nummp = sum(1 for _ in Foata_of_perm.occurrences_of(mp1)) + sum(
            1 for _ in Foata_of_perm.occurrences_of(mp2)
        )
        if numic != nummp:
            print(perm, numic)
            print(Foata_of_perm, nummp)
