#!/usr/bin/env python3
import timeit
import sys


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


def get_emails_with_filter(emails):
    newlist = list(
        filter(lambda email: email.endswith('@gmail.com'), emails)
        )
    return newlist


def main(foo, quantity):
    emails = get_list_emails()

    try:
        functions = {
            'loop': get_emails_with_loop,
            'list_comprehension': get_emails_with_list_comprehensions,
            'map': get_emails_with_map,
            'filter': get_emails_with_filter
        }

        if foo not in functions:
            raise ValueError(f"unknown function: {foo}")

        time = timeit.timeit(
            lambda: functions[foo](emails),
            number=int(quantity)
            )

        return time

    except ValueError as e:
        print(f"Value error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)

    print(main(sys.argv[1], sys.argv[2]))
