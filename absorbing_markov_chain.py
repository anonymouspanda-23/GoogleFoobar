from __future__ import division
import time
from fractions import Fraction, gcd
from itertools import starmap, compress
from operator import mul


def convert_matrix(matrix):  # convert to transition matrix
    new_matrix = []
    for index, row in enumerate(matrix):
        new_row = []
        row_total = sum(row)

        if row_total > 0:
            for value in row:
                if value == 0:
                    new_row.append(0)
                else:
                    new_row.append(Fraction(value, row_total))

        else:
            for i in range(len(row)):
                if i == index:
                    new_row.append(1)
                else:
                    new_row.append(0)

        new_matrix.append(new_row)

    return new_matrix


def progress_state(state_matrix, transition_matrix):  # for matrix multiplication
    return [sum(starmap(mul, zip(state_matrix, col))) for col in zip(*transition_matrix)]


def get_lcm(values):  # for getting common denominator
    lcm = values[0]
    for i in values[1:]:
        lcm = lcm * i / int(gcd(lcm, i))
        lcm = lcm

    return lcm


def get_end_states(matrix):  # for finding out which are transient and which are absorbing states
    states = []

    for index, row in enumerate(matrix):
        if sum(row) == 0:
            states.append(True)
        else:
            states.append(False)

    states.pop(0)
    return states


def solution(m):  # main calculations
    if m == [[0]]:
        return [1, 1]

    states = get_end_states(m)
    transition_matrix = convert_matrix(m)
    state_matrix = [0] * len(transition_matrix)
    state_matrix[0] = 1

    for i in range(10):
        state_matrix = progress_state(state_matrix, transition_matrix)

        state_matrix[0] = 0

        total = 0
        for value in state_matrix:
            total += value

        for i, value in enumerate(state_matrix):
            state_matrix[i] = value / total

            # print(state_matrix)

    state_matrix.pop(0)

    total = 0
    for value in state_matrix:
        total += value

    for i, value in enumerate(state_matrix):
        state_matrix[i] = value / total

    probabilities = []
    denominators = []
    for value in state_matrix:
        probabilities.append((value.numerator, value.denominator))
        denominators.append(value.denominator)

    lcm = get_lcm(denominators)

    results = []

    for index, value in enumerate(probabilities):
        numerator = value[0]
        denominator = value[1]

        if numerator == 0:
            if states[index]:
                results.append(0)

        else:
            if states[index]:
                multiplier = lcm / denominator
                numerator = int(numerator * multiplier)
                results.append(numerator)

    results.append(int(lcm))
    return results


def convertMatrix(transMatrix):
    """Converts transition matrix values to floats representing probabilities."""
    probMatrix = []

    for i in range(len(transMatrix)):
        row = transMatrix[i]
        newRow = []
        rowSum = sum(transMatrix[i])

        if all([v == 0 for v in transMatrix[i]]):
            for j in transMatrix[i]:
                newRow.append(0)

            newRow[i] = 1
            probMatrix.append(newRow)

        else:
            for j in transMatrix[i]:

                if j == 0:
                    newRow.append(0)

                else:
                    newRow.append(j / rowSum)
            probMatrix.append(newRow)

    return probMatrix


def terminalStateFilter(matrix):
    """Determines terminal states"""
    terminalStates = []

    for row in range(len(matrix)):

        if all(x == 0 for x in matrix[row]):
            terminalStates.append(True)

        else:
            terminalStates.append(False)

    return terminalStates


def probDistributionVector(matrix, row, timesteps):
    """Calculates the probability distribution vector for the given number of timesteps"""
    vector = matrix[row]

    for i in range(timesteps):
        newVector = [sum(starmap(mul, zip(vector, col)))
                     for col in zip(*matrix)]
        vector = newVector

    return vector


def answer(m):
    if len(m) == 1:
        return [1, 1]

    probMatrix = convertMatrix(m)
    terminalStates = terminalStateFilter(m)
    probVector = probDistributionVector(probMatrix, 0, 100)

    numerators = []
    for i in probVector:
        numerator = Fraction(i).limit_denominator().numerator
        numerators.append(numerator)

    denominators = []
    for i in probVector:
        denominator = Fraction(i).limit_denominator().denominator
        denominators.append(denominator)

    factors = [max(denominators) / x for x in denominators]
    numeratorsTimesFactors = [a * b for a, b in zip(numerators, factors)]
    terminalStateNumerators = list(compress(numeratorsTimesFactors, terminalStates))

    # append numerators and denominator to answerList
    answerlist = []
    for i in terminalStateNumerators:
        answerlist.append(i)
    answerlist.append(max(denominators))

    return list(map(int, answerlist))


if __name__ == '__main__':

    main_start = time.time()

    matrix_1 = [
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_1)
    print("Result: " + str(result))
    print("Correct: " + str(result == [0, 3, 2, 9, 14]))
    end_time = time.time()

    print("Matrix 1 time taken: " + str(end_time - start_time) + "s")

    matrix_2 = [
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_2)
    print("Result: " + str(result))
    print("Correct: " + str(result == [7, 6, 8, 21]))
    end_time = time.time()

    print("Matrix 2 time taken: " + str(end_time - start_time) + "s")

    matrix_3 = [
        [1, 2, 3, 0, 0, 0],
        [4, 5, 6, 0, 0, 0],
        [7, 8, 9, 1, 0, 0],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_3)
    print("Result: " + str(result))
    print("Correct: " + str(result == [1, 2, 3]))
    end_time = time.time()

    print("Matrix 3 time taken: " + str(end_time - start_time) + "s")

    matrix_4 = [
        [0]
    ]

    start_time = time.time()
    result = solution(matrix_4)
    print("Result: " + str(result))
    print("Correct: " + str(result == [1, 1]))
    end_time = time.time()

    print("Matrix 4 time taken: " + str(end_time - start_time) + "s")

    matrix_5 = [
        [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
        [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
        [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
        [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_5)
    print("Result: " + str(result))
    print("Correct: " + str(result == [1, 2, 3, 4, 5, 15]))
    end_time = time.time()

    print("Matrix 5 time taken: " + str(end_time - start_time) + "s")

    matrix_6 = [
        [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
        [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
        [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
        [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
        [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_6)
    print("Result: " + str(result))
    print("Correct: " + str(result == [4, 5, 5, 4, 2, 20]))
    end_time = time.time()

    print("Matrix 6 time taken: " + str(end_time - start_time) + "s")

    matrix_7 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_7)
    print("Result: " + str(result))
    print("Correct: " + str(result == [1, 1, 1, 1, 1, 5]))
    end_time = time.time()

    print("Matrix 7 time taken: " + str(end_time - start_time) + "s")

    matrix_8 = [
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_8)
    print("Result: " + str(result))
    print("Correct: " + str(result == [2, 1, 1, 1, 1, 6]))
    end_time = time.time()

    print("Matrix 8 time taken: " + str(end_time - start_time) + "s")

    matrix_9 = [
        [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
        [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_9)
    print("Result: " + str(result))
    print("Correct: " + str(result == [6, 44, 4, 11, 22, 13, 100]))
    end_time = time.time()

    print("Matrix 9 time taken: " + str(end_time - start_time) + "s")

    matrix_10 = [
        [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
        [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
        [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    start_time = time.time()
    result = solution(matrix_10)
    print("Result: " + str(result))
    print("Correct: " + str(result == [1, 1, 1, 2, 5]))
    end_time = time.time()

    print("Matrix 10 time taken: " + str(end_time - start_time) + "s")

    main_end = time.time()

    print("Total time taken: " + str(main_end - main_start) + "s")
