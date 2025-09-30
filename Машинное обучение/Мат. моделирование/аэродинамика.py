import argparse

def solve(S=None, M=None, v=None, a=None):
    if S is None:
        S = (2*M*9.8)/(1.2*v**2*a)
    if M is None:
        M = (S*1.2*v**2*a)/(2*9.8)
    if v is None:
        v = ((2*M*9.8)/(1.2*S*a))**0.5
    if a is None:
        a = (2*M*9.8)/(1.2*S*v**2)
    mu = M*9.8/v
    return S, M, v, a, mu

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--S", type=float)
    parser.add_argument("--M", type=float)
    parser.add_argument("--v", type=float)
    parser.add_argument("--a", type=float)
    args = parser.parse_args()
    res = solve(args.S, args.M, args.v, args.a)
    print("S=", res[0], "M=", res[1], "v=", res[2], "a=", res[3], "μ=", res[4])
