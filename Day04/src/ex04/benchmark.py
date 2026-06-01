#!/usr/bin/env python3

import timeit
import sys
import random
from collections import Counter


def get_generated_list():
    lst = [random.randint(0, 100) for i in range(1000000)]
    return sorted(lst)


def get_dict_my_function(lst):
    dct = {}
    for i in lst:
        if dct.get(i, False) is False:
            dct[i] = lst.count(i)
    return dct


def get_my_top(lst):
    dct = {}
    for i in lst:
        if dct.get(i, False) is False:
            dct[i] = lst.count(i)

    top_10 = dict(list(
        sorted(
            dct.items(),
            key=lambda item: item[1],
            reverse=True)
            )[:11])

    return top_10


def get_dict_with_counter(lst):
    lst_to_dict = dict(Counter(lst))

    return lst_to_dict


def get_top_counter(lst):
    dct = Counter(lst)
    dct_top_10 = dct.most_common(10)

    return dict(dct_top_10)


def main():
    lst = get_generated_list()

    time_my_function = timeit.timeit(lambda: get_dict_my_function(lst), number=1)
    time_Counter = timeit.timeit(lambda: get_dict_with_counter(lst), number=1)
    time_my_top = timeit.timeit(lambda: get_my_top(lst), number=1)
    time_Counter_top = timeit.timeit(lambda: get_top_counter(lst), number=1)

    return time_Counter, time_Counter_top, time_my_function, time_my_top


if __name__ == '__main__':
    if len(sys.argv) != 1:
        sys.exit(1)

    time_Counter, time_Counter_top, time_my_function, time_my_top = main()
    print(f"my function:{time_my_function}\nCounter: {time_Counter}\n"
          f"my top: {time_my_top}\nCounter's top: {time_Counter_top}")
