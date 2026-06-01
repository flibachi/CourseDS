#!/usr/bin/env python3
import timeit


def get_list_emails():
    emails = [
                'john@gmail.com', 'james@gmail.com',
                'alice@yahoo.com', 'anna@live.com',
                'philipp@gmail.com'
                ] * 5
    return emails


def get_emails_with_loop(emails):
    newlist = []
    for email in emails:
        if email.endswith('@gmail.com'):
            newlist.append(email)
    return newlist


def get_emails_with_list_comprehensions(emails):
    newlist = [email for email in emails if email.endswith('@gmail.com')]
    return newlist


def main():
    emails = get_list_emails()
    ex_time1 = timeit.timeit(
        lambda: get_emails_with_loop(emails),
        number=90000000
        )
    ex_time2 = timeit.timeit(
        lambda: get_emails_with_list_comprehensions(emails),
        number=90000000
        )

    m1 = "it is better to use a loop"
    m2 = "it is better to use a list comprehension"

    message = m1 if ex_time1 < ex_time2 else m2
    fastest, slowest = sorted((ex_time1, ex_time2))

    print(f'{message}\n{fastest} vs {slowest}')


if __name__ == '__main__':
    main()
