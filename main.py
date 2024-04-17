import math
import sys
import yaml
from tabulate import tabulate


def get_file_in():
    with open(sys.argv[1]) as fin:
        din = yaml.safe_load(fin)
        size = din['размерность']
        iterations = din['итерации']
        accuracy = din['точность']
        approx = din['приближение']
        matrix = din['матрица']
        return size, iterations, accuracy, approx, matrix


def check_diag(matrix, size):
    for i in range(0, size):
        if matrix[i][i] >= sum(matrix[i]) - matrix[i][i] - matrix[i][-1]:
            continue
        return False
    return True


def swap(matrix, i, size):
    temp = matrix[i]
    for j in range(0, size):
        for f in range(0, size):
            if f == i:
                if matrix[j][f] >= sum(matrix[j]) - matrix[j][f] - matrix[j][-1]:
                    matrix[i] = matrix[j]
                    matrix[j] = temp
                    return


def transform(matrix, size):
    for i in range(0, size):
        if matrix[i][i] >= sum(matrix[i]) - matrix[i][i] - matrix[i][-1]:
            continue
        print('Диагональное преобладание нарушено на ', i + 1)
        swap(matrix, i, size)
    return check_diag(matrix, size)


def conv_condition(cmatrix, size):
    summ = 0
    for i in range(0, size):
        for j in range(0, size):
            summ += cmatrix[i][j] ** 2
    return math.sqrt(summ) < 1


def get_c_matrix(matrix, size):
    cmatrix = []
    for i in range(0, size):
        buff = []
        for j in range(0, size):
            if i == j:
                buff.append(0)
            else:
                buff.append(- ((matrix[i][j]) / (matrix[i][i])))
        cmatrix.append(buff)
    return cmatrix


def get_d_vector(matrix, size):
    dvector = []
    for i in range(0, size):
        dvector.append(matrix[i][-1] / matrix[i][i])
    return dvector


def solution(matrix, iterations, accuracy, approx, size):
    print('Статус диагональной сходимости: ', transform(matrix, size))
    cmatrix = get_c_matrix(matrix, size)
    dvector = get_d_vector(matrix, size)
    print('Статус условия сходимости: ', conv_condition(cmatrix, size))
    if not conv_condition(cmatrix, size):
        exit(0)
    x = approx
    it = 0
    table = []
    while True:
        it += 1
        buff_x = []
        out_line = [it - 1]
        for i in range(0, size):
            summ = 0
            for j in range(0, len(cmatrix[i])):
                if i != j:
                    summ += matrix[i][j] / matrix[i][i] * x[j]
            xk = dvector[i] - summ
            buff_x.append(xk)
            out_line.append(xk)
        max_dif = 0
        for a in range(0, len(x)):
            if abs(x[a] - buff_x[a]) > max_dif:
                max_dif = abs(x[a] - buff_x[a])
        x = buff_x
        out_line.append(max_dif)
        table.append(out_line)
        if it == iterations:
            break
        if max_dif < accuracy:
            break
    headers = ['k']
    for i in range(0, size):
        headers.append('x_' + str(i))
    headers.append('MAX_DIF')
    print(tabulate(table, headers=headers))


def main():
    size = 0
    iterations = 0
    accuracy = 0.01
    approx = []
    matrix = []
    if len(sys.argv) > 1:
        size, iterations, accuracy, approx, matrix = get_file_in()
    else:
        size = int(input('Введите размерность матрицы: '))
        iterations = int(input('Введите максимальное количество итераций: '))
        accuracy = float(input('Введите необходимую точность результата'))
        buff = input('Введите начальное приближение (Через пробел): ').strip().split(' ')
        for b in buff:
            approx.append(float(b))
        for i in range(0, size):
            buff = input(
                'Введите' + str(i + 1) + '-ю строку матрицы СЛАУ (Через пробел с правой частью): ').strip().split(' ')
            if len(buff) != size + 1:
                raise ValueError('Введённая строка не соответствует указанной размерности')
            line = []
            for b in buff:
                line.append(float(b))
            matrix.append(line)
    if size > 20:
        raise ValueError('Размерность матрицы не может превышать 20')
    elif size < 2:
        raise ValueError('Размерность матрицы не может быть меньше 2')
    if iterations < 0:
        raise ValueError('Отрицательное количество итераций')
    if accuracy <= 0:
        raise ValueError('Точность должна быть указана положительно')

    if len(approx) != size:
        raise ValueError('Размерность начального приближения не соответствует указанной размерности')

    if len(matrix) != size:
        raise ValueError('Размерность матрицы не соответствует указанной')
    for line in matrix:
        if len(line) != size + 1:
            raise ValueError('Нарушена размерность матрицы в строке')

    solution(matrix, iterations, accuracy, approx, size)


if __name__ == '__main__':
    main()
