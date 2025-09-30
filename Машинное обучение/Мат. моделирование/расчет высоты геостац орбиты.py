import math

def geostat_height(T, R, G, M):
    return ((G * M * (T**2)) / (4 * math.pi**2))**(1/3) - R

def num_satellites(R, h):
    return math.ceil((2 * math.pi * (R + h)) / (2 * R))


planets = {
    "Земля": {"R": 6.371e6, "M": 5.972e24, "T": 86164},
    "Марс": {"R": 3.389e6, "M": 6.39e23, "T": 88642},
    "Венера": {"R": 6.052e6, "M": 4.867e24, "T": 209967}
}

G = 6.67430e-11

for name, p in planets.items():
    h = geostat_height(p["T"], p["R"], G, p["M"])
    n = num_satellites(p["R"], h)
    print(f"{name}: h = {h/1000:.2f} км, спутников = {n}")
