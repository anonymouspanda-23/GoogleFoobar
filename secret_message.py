from itertools import permutations
import time


def func_v1(plate_number_list):
    max_divisible = 0
    plate_number_list.sort(reverse=True)

    for length in range(len(plate_number_list), 1, -1):
        perms = list(permutations(plate_number_list, length))

        for index, perm in enumerate(perms):
            perm = list(perm)

            new_number = 0
            for digit in perm:
                new_number = new_number * 10 + digit

            perms[index] = new_number

        perms.sort(reverse=True)

        for perm in perms:
            if perm % 3 == 0:
                return perm

    return max_divisible


def func_v2(l):
    list(l)
    plate_numbers = l[:]

    remainder = sum(plate_numbers) % 3

    while remainder and plate_numbers:
        if remainder == 1:
            to_remove = set(plate_numbers) & {1, 4, 7}

            if not to_remove:
                to_remove = set(plate_numbers) & {2, 5, 8}

        elif remainder == 2:
            to_remove = set(plate_numbers) & {2, 5, 8}

            if not to_remove:
                to_remove = set(plate_numbers) & {1, 4, 7}

        plate_numbers.remove(min(to_remove))
        remainder = sum(plate_numbers) % 3

    plate_numbers.sort(reverse=True)
    number = ''.join(str(digit) for digit in plate_numbers)
    return int(number) if number else 0


if __name__ == '__main__':
    values_list = [1]

    v1_start_time = time.time()
    max_val = func_v1(values_list)
    print(max_val)
    v1_end_time = time.time()

    print(f"Time taken for v1: {v1_end_time - v1_start_time}s.")

    v2_start_time = time.time()
    max_val = func_v2(values_list)
    print(max_val)
    v2_end_time = time.time()

    print(f"Time taken for v2: {v2_end_time - v2_start_time}s.")
