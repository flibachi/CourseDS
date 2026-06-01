from random import randint
import logging
import requests
from config import CHAT_ID, URL, SUCCESS_MSG, ERROR_MSG


class Research:
    def __init__(self, path):
        self.path = path
        logging.info(f"Research initialized with path <{path}>")

    def file_reader(self, has_header=True):
        logging.debug(f"Reading file (header={has_header})")
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
                logging.error(f"Incorrect number of lines {len(lst)}")
                raise ValueError(f"Incorrect number of lines {len(lst)}")

            newlist = self._lines_after_the_header(shift, lst)
            logging.info("The contents of the file are correct")
            return newlist

    def _read_header(self, lst):
        logging.info("Reading header in lst")
        firstline = lst[0].strip()

        if not firstline or firstline.count(',') != 1:
            logging.error("Wrong header")
            raise ValueError("Wrong header")

        fields = firstline.split(',')

        if not fields[0].strip() or not fields[1].strip():
            logging.error("Wrong header")
            raise ValueError("Wrong header")

        if fields[0] in '01' or fields[1] in '01':
            logging.error("Invalid header")
            raise ValueError("Invalid header")
        logging.info("Successfully read header")

    def _lines_after_the_header(self, shift, lst):
        logging.info("Reading lines after header")
        newlist = []
        for i, line in enumerate(lst[shift:], start=shift+1):
            newline = line.strip()

            if not newline or newline.count(',') != 1:
                logging.error(f"Line {i} error")
                raise ValueError("Incorrect string format")

            linefields = newline.split(',')
            field1 = linefields[0].strip()
            field2 = linefields[1].strip()

            if not field1 or not field2:
                logging.error(f"Line {i} error")
                raise ValueError("Missing value in line")

            for num in linefields:
                if num.strip() not in {'0', '1'}:
                    logging.error(f"Line {i} error")
                    raise ValueError("Possible values are only 0 and 1")

            if field1 == field2:
                logging.error(f"Line {i} error")
                raise ValueError("Values must be different")
            newlist.append(list(map(int, line.split(','))))
        logging.info("Successfully read lines after the header")
        return newlist

    def _file_existence(self):
        filepath = f'../{self.path}'
        try:
            with open(filepath):
                pass
        except FileNotFoundError:
            logging.error(f"File not found <{filepath}>")
            raise FileNotFoundError(f"File not found <{filepath}>")

        logging.info("Successfully read file")

        return filepath

    def send_message_to_bot(self, report_success):
        logging.debug(f"Creating telegram message, report_success={report_success}")

        message = SUCCESS_MSG if report_success else ERROR_MSG

        params = {
            "chat_id": CHAT_ID,
            "text": message
        }

        try:
            requests.post(URL, params=params)
        except Exception:
            logging.error(f"Bad telegram request: {URL}")

    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.info(f"Calculations initialized with data: {data}")

        def counts(self):
            heads = 0
            tails = 0
            for half in self.data:
                if half == [1, 0]:
                    heads += 1
                elif half == [0, 1]:
                    tails += 1
                else:
                    logging.error(f"Invalid data pair {half}")
                    raise ValueError(f"Invalid data pair {half}")
            logging.info("Heads and tails have been successfully counted")
            return heads, tails

        def fractions(self, heads, tails):
            total = heads + tails
            if total == 0:
                return 0, 0
            res1 = (heads / total) * 100
            res2 = (tails / total) * 100
            logging.info("The percentage has been calculated successfully")
            return res1, res2

    class Analytics(Calculations):
        def __init__(self, data):
            super().__init__(data)

        def predict_random(self, num_of_steps):
            logging.info(f"Generating {num_of_steps} predictions")

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
                logging.error(f"Incorrect number:{num_of_steps}")
                raise ValueError(f"Incorrect number:{num_of_steps}")
            logging.debug(f"Predictions: {predictions}")
            return predictions

        def predict_last(self):
            return self.data[-1]

        def save_file(self, data, f_name, f_type='txt'):
            filename = f"{f_name}.{f_type}"
            with open(filename, 'w', encoding='utf=8') as file:
                file.write(str(data))
            logging.info(f"File saved <{filename}>")
