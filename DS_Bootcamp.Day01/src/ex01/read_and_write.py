def func():
    with open('ds.csv', 'r', encoding='utf-8') as csv_file, open('ds.tsv', 'w', encoding='utf-8') as tsv_file:
        quotes = 0
        for line in csv_file:
            for l in line:
                if l == '"':
                    tsv_file.write(l)
                    quotes += 1
                elif l == ',' and (quotes % 2 == 0):
                    tsv_file.write('\t')
                else:
                    tsv_file.write(l)         

if __name__ == '__main__':  
    func()