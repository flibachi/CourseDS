import sys
import os


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        filepath = self._file_existence()

        with open(filepath, 'r', encoding='utf-8') as csv_file:
            lst = csv_file.readlines()

            if len(lst) < 2:
                raise ValueError("Incorrect number of lines")
            firstline = lst[0].strip()

            if not firstline or firstline.count(',') != 1:
                raise ValueError("Wrong header")
            fields = firstline.split(',')

            if not fields[0].strip() or not fields[1].strip():
                raise ValueError("Incomplete header")

            if fields[0] in '01' or fields[1] in '01':
                raise ValueError("Invalid header")

            for line in lst[1:]:
                newline = line.strip()

                if not newline or newline.count(',') != 1:
                    raise ValueError("Incorrect string format")
                linefields = newline.split(',')

                if not linefields[0].strip() or not linefields[1].strip():
                    raise ValueError("Missing value in line")

                for num in linefields:
                    if num.strip() not in {'0', '1'}:
                        raise ValueError("Possible values are only 0 and 1")
                if linefields[0] == linefields[1]:
                    raise ValueError("Values сannot be different and equal")

            return lst

    def _file_existence(self):
        filepath = f"../{self.path}"
        if not os.path.isfile(filepath):
            raise FileNotFoundError("File not found")
        return filepath


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: first_construction.py <file>")
        sys.exit(1)

    try:
        researcher = Research(sys.argv[1])
        print(''.join(researcher.file_reader()))
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
