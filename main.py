from __future__ import annotations

import re


class Matrix:
    def __init__(self, row=None, number=None, column=None, rows_count=None, columns_count=None):
        if row is None or number is None or column is None or rows_count is None or columns_count is None:
            self.row = []
            self.column = []
            self.number = []
            self.rows_count = 0
            self.columns_count = 0
        else:
            self.row = row
            self.column = column
            self.number = number
            self.rows_count = rows_count
            self.columns_count = columns_count

    def parse(self, string):
        self.row = []
        self.column = []
        self.number = []
        self.rows_count = 0
        self.columns_count = 0
        string = string[1:-1]
        rows = re.split(r"\s(?=\[)", string)
        number_count = 0
        for i, row in enumerate(rows):
            self.row.append(number_count)
            if row[-1] == ',':
                row = row[1:-2].split(", ")
            else:
                row = row[1:-1].split(", ")
                self.columns_count = len(row)
            for j, number in enumerate(row):
                if number == '0':
                    continue
                number_count += 1
                self.number.append(float(number))
                self.column.append(j)
        self.row.append(number_count)
        self.rows_count = len(rows)

    def transpose(self) -> Matrix:
        new_number = [[] for i in range(self.columns_count)]
        new_column = [[] for i in range(self.columns_count)]

        for i in range(self.rows_count):
            numbers_count = self.row[i + 1] - self.row[i]
            for j in range(numbers_count):
                index_of_number = self.row[i] + j
                new_number[self.column[index_of_number]].append(self.number[index_of_number])
                new_column[self.column[index_of_number]].append(i)

        row = [0]
        for element in new_column:
            row.append(row[-1] + len(element))

        column = []
        for element in new_column:
            column.extend(element)

        number = []
        for element in new_number:
            number.extend(element)

        result = Matrix(row, number, column, self.columns_count, self.rows_count)

        return result

    def get_row(self, row: int) -> Matrix:
        number = self.number[self.row[row]:self.row[row + 1]]
        column = self.column[self.row[row]:self.row[row + 1]]
        row = self.row[row:row + 2]
        for i in range(len(row)):
            row[i] = row[i] - row[0]

        result = Matrix(row, number, column, 1, self.columns_count)
        return result

    def append_row(self, row_vector: Matrix) -> Matrix:
        number = self.number
        number.extend(row_vector.number)
        column = self.column
        column.extend(row_vector.column)
        row = self.row
        row.append(row[-1] + row_vector.row[-1])

        result = Matrix(row, number, column, self.rows_count + 1, self.columns_count)

        return result

    def multiply_vector(self, vector: Matrix) -> Matrix:
        numbers_count_of_vector = b.row[-1]
        number = []
        column = []

        for i in range(self.rows_count):
            numbers_count_of_matrix = self.row[i + 1] - self.row[i]

            index_matrix = 0
            index_vector = 0

            res = 0

            while index_matrix < numbers_count_of_matrix and index_vector < numbers_count_of_vector:
                if self.column[self.row[i] + index_matrix] == vector.column[index_vector]:
                    res += self.number[self.row[i] + index_matrix] * vector.number[index_vector]
                    index_matrix += 1
                    index_vector += 1
                elif self.column[self.row[i] + index_matrix] < vector.column[index_vector]:
                    index_matrix += 1
                elif self.column[self.row[i] + index_matrix] > vector.column[index_vector]:
                    index_vector += 1

            if res != 0:
                number.append(res)
                column.append(i)

        row = [0, len(number)]

        result = Matrix(row, number, column, 1, self.rows_count)
        return result

    def multiply_transposed(self, b_transposed: Matrix) -> Matrix:
        row_vector = b_transposed.get_row(0)
        self.multiply_vector(row_vector)

        result = self.multiply_vector(row_vector)

        for i in range(1, b_transposed.rows_count):
            row_vector = b_transposed.get_row(i)
            res = self.multiply_vector(row_vector)
            result = result.append_row(res)

        return result

    def multiply(self, b: Matrix) -> Matrix:
        if self.columns_count != b.rows_count:
            print("can't multiply matrix with different dimensions (empty matrix returned)")
            return Matrix()
        if self.columns_count == 0 or b.columns_count == 0:
            print("can't multiply empty matrix (empty matrix returned)")
            return Matrix()

        b_transposed = b.transpose()

        result = self.multiply_transposed(b_transposed)

        result = result.transpose()

        return result

    def multiply_by_const(self, const: float) -> Matrix:
        number = self.number
        for i in range(len(self.number)):
            number[i] *= const

        result = Matrix(self.row, number, self.column, self.rows_count, self.columns_count)

        return result

    def plus(self, b: Matrix) -> Matrix:
        if self.columns_count != b.columns_count or self.rows_count != b.rows_count:
            print("can't plus matrix with different dimensions (empty matrix returned)")
            return Matrix()

        number = []
        column = []
        row = []
        numbers_count = 0
        for i in range(self.rows_count):
            row.append(numbers_count)
            numbers_count_of_a = self.row[i + 1] - self.row[i]
            numbers_count_of_b = b.row[i + 1] - b.row[i]

            index_a = 0
            index_b = 0

            while index_a < numbers_count_of_a or index_b < numbers_count_of_b:
                if (self.column[self.row[i] + index_a] == b.column[b.row[i] + index_b]) and (
                        index_b < numbers_count_of_b) and (index_a < numbers_count_of_a):
                    res = self.number[self.row[i] + index_a] + b.number[b.row[i] + index_b]
                    number.append(res)
                    column.append(self.column[self.row[i] + index_a])
                    index_a += 1
                    index_b += 1
                elif self.column[self.row[i] + index_a] < b.column[b.row[i] + index_b] or index_b >= numbers_count_of_b:
                    number.append(self.number[self.row[i] + index_a])
                    column.append(self.column[self.row[i] + index_a])
                    index_a += 1
                elif self.column[self.row[i] + index_a] > b.column[b.row[i] + index_b] or index_a >= numbers_count_of_a:
                    number.append(b.number[b.row[i] + index_b])
                    column.append(b.column[b.row[i] + index_b])
                    index_b += 1
                numbers_count += 1
        row.append(numbers_count)

        result = Matrix(row, number, column, self.rows_count, self.columns_count)

        return result

    def to_string(self) -> str:
        # inefficient way, but 100% work
        #
         matrix = [[0 for j in range(self.columns_count)] for i in range(self.rows_count)]
         for i, row in enumerate(self.row[:-1]):
             number_count = self.row[i + 1] - self.row[i]
             for j in range(self.row[i], self.row[i] + number_count):
                 matrix[i][self.column[j]] = self.number[j]
         return str(matrix)

        # efficient way, but 99% work 🥲 
        #result = "["
        #row = []
        #for i in range(self.rows_count):
        #   index_of_number = self.row[i]
        #  for j in range(self.columns_count):
        #     if index_of_number != self.row[-1] and j == self.column[index_of_number] and j < self.row[i + 1]:
        #        row.append(self.number[index_of_number])
        #       index_of_number += 1
        #  else:
        #     row.append(0)
        # if i != self.rows_count - 1:
        #    result += str(row) + ", "
        # else:
        #    result += str(row) + "]"
        #row.clear()
        # return result


f = open("matrix/input.txt", "r")
output = open("matrix/output.txt", "w")
a = Matrix()
b = Matrix()

# simple multiply
a.parse(f.readline().strip())
b.parse(f.readline().strip())
output.write(a.multiply(b).to_string() + "\n")


# multiply on inverse matrix
a.parse(f.readline().strip())
b.parse(f.readline().strip())
output.write(a.multiply(b).to_string() + "\n")

# multiply by zero matrix
a.parse(f.readline().strip())
b.parse(f.readline().strip())
output.write(a.multiply(b).to_string() + "\n")

# multiply rectangle matrix
a.parse(f.readline().strip())
b.parse(f.readline().strip())
output.write(a.multiply(b).to_string() + "\n")

# sum of matrix
a.parse(f.readline().strip())
b.parse(f.readline().strip())
output.write(a.plus(b).to_string() + "\n")

# multiply on const
a.parse(f.readline().strip())
output.write(a.multiply_by_const(2).to_string() + "\n")

f.close()
output.close()

string = [1, 2, 3]

print(string)
