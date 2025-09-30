def quadratic(a, b, c):
    if a == 0 and b == 0 and c == 0:
        return "Любое x"
    if a == 0 and b == 0:
        return "Нет решений"
    if a == 0:
        return f"x = {-c/b}"
    D = b**2 - 4*a*c
    if D < 0:
        return "Нет действительных решений"
    if D == 0:
        return f"x = {-b/(2*a)}"
    return f"x1 = {(-b+ D**0.5)/(2*a)}, x2 = {(-b- D**0.5)/(2*a)}"

def power3(n):
    if n == 1:
        return True
    if n%3 != 0 or n == 0:
        return False
    return power3(n//3)

print(quadratic(1, -3, 2))
print(power3(27))
