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


def has_increasing_cycle(perm, i):
    cd = perm.cycle_decomp()
    for c in cd:
        if len(c) == i:
            if cycle_is_increasing(c):
                return True
    return False


def cycle_is_increasing(c):
    fc = fix_cycle(c)
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


def cycle_is_sorted_increasing(c):
    fc = sorted(fix_cycle(c))
    for j in range(len(fc) - 1):
        if fc[j + 1] - fc[j] != 1:
            return False
    return True


q = 3
# auto_bisc(lambda perm: not has_increasing_cycle(inverse_Foata(perm), q))
auto_bisc(lambda perm: not has_increasing_sorted_cycle(inverse_Foata(perm), q))
