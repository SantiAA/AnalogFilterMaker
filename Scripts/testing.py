
def shift_stages(arr, indexes: list, left):
    """ Shifts the stages indicated at the indexes list. Shifts left if left == True,shifts rigth otherwise"""
    if left:
        step = -1
        i_lim = 0
        i = len(arr)
    else:
        step = 1
        i_lim = len(arr)
        i = 0
        # i = len(indexes)
        rep = step
    while i != i_lim:
        if i in indexes:
            while i + rep in indexes:
                rep += step
            arr[i], arr[i + rep] = (arr[i + rep], arr[i])
        i += step
        rep = step
    print("After: " + str(arr))

if __name__ == "__main__":
 #    p = [-1.91033347e+00+1.23836234j, -1.91033347e+00-1.23836234j,
 #  1.91033347e+00+1.23836234j,  1.91033347e+00-1.23836234j,
 # -1.34132767e+00+1.59051334j, -1.34132767e+00-1.59051334j,
 #  1.34132767e+00+1.59051334j,
 # -7.35074235e-01+1.9413347j,  -7.35074235e-01-1.9413347j,
 #  7.35074235e-01+1.9413347j,   7.35074235e-01-1.9413347j,
 # -5.55111512e-17+2.07692735j]
    # print("pairs: " + str(_agrup_poles(p)))
    p = [1, 2, 3, 4, 5, 6, 7]
    print("Before: " + str(p))
    shift_stages(p, [1, 2], False)

