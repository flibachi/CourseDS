import sys
import os


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        filepath = self._file_existence()

        with open(filepath, 'r', encoding='utf-8') as csv_file:
            lst = csv_file.readlines()

            min_line = 1
            shift = 0

            if has_header:
                self._read_header(lst)
                shift = 1
                min_line = 2

            if len(lst) < min_line:
                raise ValueError("Incorrect number of lines")

            newlist = self._lines_after_the_header(shift, lst)

            return newlist

    def _read_header(self, lst):
        firstline = lst[0].strip()

        if not firstline or firstline.count(',') != 1:
            raise ValueError("Wrong header")

        fields = firstline.split(',')

        if not fields[0].strip() or not fields[1].strip():
            raise ValueError("Wrong header")

        if fields[0] in '01' or fields[1] in '01':
            raise ValueError("Invalid header")

    def _lines_after_the_header(self, shift, lst):
        newlist = []
        for line in lst[shift:]:
            newline = line.strip()

            if not newline or newline.count(',') != 1:
                raise ValueError("Incorrect string format")

            linefields = newline.split(',')
            field1 = linefields[0].strip()
            field2 = linefields[1].strip()

            if not field1 or not field2:
                raise ValueError("Missing value in line")

            for num in linefields:
                if num.strip() not in {'0', '1'}:
                    raise ValueError("Possible values are only 0 and 1")

            if field1 == field2:
                raise ValueError("Values сannot be different and equal")
            newlist.append(list(map(int, line.split(','))))
        return newlist

    def _file_existence(self):
        filepath = f"../{self.path}"
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found <{self.path}>")
        return filepath

    class Calculations():
        @staticmethod
        def counts(data):
            heads = 0
            tails = 0
            for half in data:
                if half == [1, 0]:
                    heads += 1
                elif half == [0, 1]:
                    tails += 1
                else:
                    raise ValueError(f"Invalid data pair {half}")
            return heads, tails

        @staticmethod
        def fractions(heads, tails):
            total = heads + tails
            if total == 0:
                return 0, 0
            res1 = (heads / total) * 100
            res2 = (tails / total) * 100
            return res1, res2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: first_nest.py <file>")
        sys.exit(1)

    try:
        researcher = Research(sys.argv[1])
        data = researcher.file_reader(True)
        print(data)

        heads, tails = Research.Calculations.counts(data)
        print(heads, tails)

        fraction1, fractions2 = Research.Calculations.fractions(heads, tails)
        print(fraction1, fractions2)

    except FileNotFoundError as e:
        print(f"File error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"Data error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
