class Must_read:
    try:
        with open('../data.csv', 'r', encoding='utf-8') as csv_file:
            print(csv_file.read())
    except:
        print("File not found")


if __name__ == "__main__":
    Must_read
