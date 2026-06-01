import sys

def names_extractor(path):
    with open(path, 'r', encoding='utf-8') as txt_file:
        with open('employees.tsv', 'w', encoding='utf-8') as tsv_file:
            tsv_file.write(f"Name\tSurname\tE-mail\n")
            for email in txt_file:
                name = email[:email.find('.')]
                surname = email[email.find('.') + 1:email.find('@')]
                tsv_line = f"{name.title()}\t{surname.title()}\t{email}"
                tsv_file.write(tsv_line)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Ошибка, пример использования: python names_extractor.py <file.txt>")
        sys.exit(1)
    
    names_extractor(sys.argv[1])