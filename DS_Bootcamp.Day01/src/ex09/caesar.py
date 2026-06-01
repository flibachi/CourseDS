import sys

def cipher(
        line,
        n):
    result = []
    for ch in line:
        if ch.islower():
            result.append(chr((ord(ch) - 97 + n) % 26 + 97))
        elif ch.isupper():
            result.append(chr((ord(ch) - 65 + n) % 26 + 65))
        else:
            result.append(ch)
    return ''.join(result)

def func_arg(args):
    action = args[1]
    line = args[2]
    shift = int(args[3])
    if action == "encode":
        res = cipher(line, shift)
        print(res)
    elif action == "decode":
        res = cipher(line, -shift)
        print(res)
    else:
        print("Use 'encode' or 'decode'")

if __name__=="__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 caesar.py encode 'example.line' 2")
        sys.exit(1)   

    if any(i in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" for i in sys.argv[2]):
        print("Error: unknown language or incorrectly entered shift")
        sys.exit(1) 
    try:
        shift = int(sys.argv[3])

    except ValueError:
        print("Error: use shift number type <int>")
        sys.exit(1)

    func_arg(sys.argv)