import sys

def clients():
    return set(['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com'])

def participants():
    return set(['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com'])
    
def recipients():
    return set(['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is'])

def no_recipients():
    r, c = recipients(), clients()
    for email in c:
        if email not in r:
            print(email)

def no_clients():
    p, c = participants(), clients()
    for email in p:
        if email not in c:
            print(email)

def no_participants():
    p, c = participants(), clients()
    for email in c:
        if email not in p:
            print(email)

def func(cmd):
    if cmd ==  "call_center":
        return no_recipients()
    elif cmd == "potential_clients":
        return no_clients()
    elif cmd == "loly_program":
        return no_participants()
    else:
        print ("Неверно введена команда. Вот список существующих: call_center, potential_clients, loly_program")
        sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Введите одну из существующих команд \"call_center\", \"potential_clients\", \"loly_program\"")
        sys.exit(1)
 
    func(sys.argv[1])