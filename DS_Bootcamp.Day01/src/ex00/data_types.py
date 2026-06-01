def data_types():
    values = [0, "0", 0.0, bool(0), [0], {'a':0, 'b':0}, (0, 0), set('0')]
    print(f"[{', '.join(map(lambda x: type(x).__name__, values))}]")
    return 0


if __name__ == '__main__':
    data_types()