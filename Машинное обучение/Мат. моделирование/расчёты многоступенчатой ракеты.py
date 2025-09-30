import math

def rocket(m0, dv, ve, alpha, stages):
    results = []
    m = m0
    for i in range(stages):
        dm = m * (1 - math.exp(-dv/(ve*stages)))
        ms = alpha * dm
        mp = (1-alpha) * dm
        results.append((i+1, m, ms, mp))
        m -= dm
    return results


for stages in [2, 3]:
    print(f"\n{stages}-ступенчатая ракета:")
    res = rocket(500000, 9600, 3100, 0.15, stages)
    for r in res:
        print(f"Ступень {r[0]}: масса {r[1]:.0f}, конструкция {r[2]:.0f}, топливо {r[3]:.0f}")
