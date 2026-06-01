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


def get_emails_with_map(emails):
    newlist = list(
        map(lambda email: email.endswith('@gmail.com'), emails)
        )
    return newlist


def main():
    emails = get_list_emails()

    time_loop = timeit.timeit(
        lambda: get_emails_with_loop(emails),
        number=90000000
        )
    time_comprehensions = timeit.timeit(
        lambda: get_emails_with_list_comprehensions(emails),
        number=90000000
        )
    time_map = timeit.timeit(
        lambda: get_emails_with_map(emails),
        number=90000000
        )

    m1 = "it is better to use a loop"
    m2 = "it is better to use a list comprehension"
    m3 = "it is better to use a map"

    if time_map < time_comprehensions and time_map < time_loop:
        message = m3
    elif time_comprehensions <= time_loop:
        message = m2
    else:
        message = m1

    fastest, average, slowest = sorted(
        (time_loop, time_comprehensions, time_map)
        )

    print(f'{message}\n{fastest} vs {average} vs {slowest}')


if __name__ == '__main__':
    main()
