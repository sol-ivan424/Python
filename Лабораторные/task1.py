from math import ceil


def main(tt):
    ii = {abs(t) for t in tt if -97 <= t <= 44}
    ee = {abs(t) - 5 * t for t in tt if -69 <= t <= 37}
    bb = {i * e for i in ii for e in ee if i > e}

    cc = len(ee) + sum(ceil(b / 7) for b in bb)
    return cc