import sys
from random import randint


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
                raise ValueError("Values must be different")
            newlist.append(list(map(int, line.split(','))))
        return newlist

    def _file_existence(self):
        filepath = f'../{self.path}'
        try:
            with open(filepath):
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found <{filepath}>")
        return filepath

    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            eagle = 0
            tails = 0
            for half in self.data:
                if half == [1, 0]:
                    eagle += 1
                elif half == [0, 1]:
                    tails += 1
                else:
                    raise ValueError(f"Invalid data pair {half}")
            return eagle, tails

        def fractions(self, eagle, tails):
            total = eagle + tails
            if total == 0:
                return 0, 0
            res1 = (eagle / total) * 100
            res2 = (tails / total) * 100
            return res1, res2

    class Analytics(Calculations):
        def __init__(self, data):
            super().__init__(data)

        def predict_random(self, num_of_steps):
            if num_of_steps > 0:
                predictions = []
                for _ in range(num_of_steps):
                    two = [randint(0, 1)]
                    if two[0] == 0:
                        two.append(1)
                    else:
                        two.append(0)
                    predictions.append(two)
            else:
                raise ValueError(f"Incorrect number:{num_of_steps}")
            return predictions

        def predict_last(self):
            return self.data[-1]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: first_child.py <file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        researcher = Research(filepath)
        data = researcher.file_reader(True)
        print(data)

        calculations = researcher.Analytics(data)

        eagle, tails = calculations.counts()
        print(eagle, tails)

        fract1, fract2 = calculations.fractions(eagle, tails)
        print(fract1, fract2)

        prediction = calculations.predict_random(3)
        print(prediction)

        last_prediction = calculations.predict_last()
        print(last_prediction)

    except FileNotFoundError as e:
        print(f"File error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"Data error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
