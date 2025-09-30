def minor(matrix, i, j):
    """Вычисляет минор матрицы после удаления строки i и столбца j."""
    return [row[:j] + row[j+1:] for idx, row in enumerate(matrix) if idx != i]

def determinant(matrix):
    #Рекурсивное вычисление определителя матрицы
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for j in range(n):
        det += ((-1) ** j) * matrix[0][j] * determinant(minor(matrix, 0, j))
    return det

def cofactor_matrix(matrix):
    #Вычисляет матрицу алгебраических дополнений
    n = len(matrix)
    cofactors = []
    for i in range(n):
        row = []
        for j in range(n):
            minor_det = determinant(minor(matrix, i, j))
            row.append(((-1) ** (i + j)) * minor_det)
        cofactors.append(row)
    return cofactors

def transpose(matrix):
    #Транспонирует матрицу
    return [list(row) for row in zip(*matrix)]

def inverse_matrix(matrix):
    #Вычисляет обратную матрицу.
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Матрица вырождена, решения нет!")
    cofactors = cofactor_matrix(matrix)
    adjugate = transpose(cofactors)
    return [[adjugate[i][j] / det for j in range(len(matrix))] for i in range(len(matrix))]

def multiply_matrix_vector(matrix, vector):
    #Умножает матрицу на вектор#
    return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]

def solve_system(A, B):
    #Решает СЛАУ AX=B
    inv_A = inverse_matrix(A)
    return multiply_matrix_vector(inv_A, B)


if __name__ == "__main__":
    # Ввод матрицы A и вектора B
    n = int(input("Введите размерность матрицы: "))
    A = []
    print("Введите коэффициенты матрицы A:")
    for _ in range(n):
        A.append(list(map(float, input().split())))

    print("Введите элементы вектора B:")
    B = list(map(float, input().split()))

    try:
        X = solve_system(A, B)
        print("Решение системы X:")
        for x in X:
            print(round(x, 5))
    except ValueError as e:
        print(e)
