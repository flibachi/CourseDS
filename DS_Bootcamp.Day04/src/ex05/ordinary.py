#!/usr/bin/env python3
import sys
import resource


def main(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    file_path = sys.argv[1]

    lst = main(file_path)

    for line in lst:
        pass

    data = resource.getrusage(resource.RUSAGE_SELF)
    time = data.ru_utime + data.ru_stime
    max_memory = data.ru_maxrss * 1e-6

    print(f"Peak Memory Usage = {max_memory:.3f}GB\n"
          f"User Mode Time + System Mode Time = {time:.2f}s")
