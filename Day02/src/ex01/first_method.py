class Research:
    def file_reader():
        try:
            with open('../data.csv', 'r', encoding='utf-8') as csv_file:
                output = (csv_file.read())
        except FileNotFoundError:
            output = "File not found"
        return output


if __name__ == "__main__":
    print(Research.file_reader())
