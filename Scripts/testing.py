

def _agrup_poles2(p):
    pairs = []
    print("p: " + str(p))
    p.sort(key=lambda x: x.real)  # ordeno por parte real creciente
    print("sorted p: " + str(p))
    i = 1
    while i <= len(p):
        if (abs(p[i - 1].real - p[i].real) < 1e-10) and (abs(p[i - 1].imag + p[i].imag) < 1e-10):
            pairs.append([p[i - 1], p[i]])
            i += 1
        else:
            pairs.append([p[i - 1]])
        i += 1
    return pairs


def _agrup_poles(p):
    pairs = []
    print("p: " + str(p))
    p.sort(key=lambda x: x.real)  # ordeno por parte real creciente
    print("sorted p: " + str(p))
    while len(p):
        len_in = len(pairs)
        for i in range(1, len(p)):
            if (abs(p[0].real - p[i].real) < 1e-10) and (abs(p[0].imag + p[i].imag) < 1e-10):
                pairs.append([p[0], p[i]])
                p.remove(p[i])
                break
        if len_in == len(pairs):    # si no le encontre un conjugado
            pairs.append([p[0]])    # no lo tiene :(
        p.remove(p[0])
    return pairs



if __name__ == "__main__":
    p = [-1.91033347e+00+1.23836234j, -1.91033347e+00-1.23836234j,
  1.91033347e+00+1.23836234j,  1.91033347e+00-1.23836234j,
 -1.34132767e+00+1.59051334j, -1.34132767e+00-1.59051334j,
  1.34132767e+00+1.59051334j,
 -7.35074235e-01+1.9413347j,  -7.35074235e-01-1.9413347j,
  7.35074235e-01+1.9413347j,   7.35074235e-01-1.9413347j,
 -5.55111512e-17+2.07692735j]
    # print("pairs: " + str(_agrup_poles(p)))
    p = []
    for i in range(5):
        p += []
    p += [3,3]
    print(p)
