import sys

def letter_starter(email):
    file = 'employees.tsv'
    with open (file, 'r', encoding='utf-8') as tsv_file:
        for line in tsv_file:
            if email in line:
                name = line[:line.find('\t')]
                print(f"Dear {name.title()}, welcome to our team. We are sure that it will be a pleasure to work with you."
                "That’s a precondition for the professionals that our company hires.")
                return
            
if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Ошибка, пример использования: python letter_starter.py <email>")
        sys.exit(1)
    letter_starter(sys.argv[1])

