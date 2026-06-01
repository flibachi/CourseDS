#!/usr/bin/env python3
import timeit
import sys
from functools import reduce


def get_sum_with_loop(counts):
    res = 0

    for i in range(1, counts+1):
        res = res + i*i

    return res


def get_sum_with_reduce(counts):
    numbers = list(range(1, counts+1))
    res = 0
    res = reduce(lambda x, y: x+y*y, numbers)

    return res


def main(foo, quantity, counts):
    counts = int(counts)
    try:
        functions = {
            'loop': get_sum_with_loop,
            'reduce': get_sum_with_reduce
        }

        if foo not in functions:
            raise ValueError(f"unknown function: {foo}")

        time = timeit.timeit(
            lambda: functions[foo](counts),
            number=int(quantity)
            )

        return time

    except ValueError as e:
        print(f"Value error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(1)

    print(main(sys.argv[1], sys.argv[2], sys.argv[3]))
