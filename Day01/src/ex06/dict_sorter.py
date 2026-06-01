def list_of_countries():
    list = [
    ('Russia', '25'),
    ('France', '132'),
    ('Germany', '132'),
    ('Spain', '178'),
    ('Italy', '162'),
    ('Portugal', '17'),
    ('Finland', '3'),
    ('Hungary', '2'),
    ('The Netherlands', '28'),
    ('The USA', '610'),
    ('The United Kingdom', '95'),
    ('China', '83'),
    ('Iran', '76'),
    ('Turkey', '65'),
    ('Belgium', '34'),
    ('Canada', '28'),
    ('Switzerland', '26'),
    ('Brazil', '25'),
    ('Austria', '14'),
    ('Israel', '12')
    ]
    return list

def converter_to_dict(lst):
    converted_dict = {key: int(value) for key, value in lst}
    return converted_dict

def dict_sorter(dict_for_sort):
    sorted_dict = sorted(dict_for_sort.items(), key=lambda x: (-x[1], x[0]))
    return sorted_dict

if __name__ == '__main__':
    lst = list_of_countries()
    converted_dict = converter_to_dict(lst)
    sorted_dict_to_value = dict_sorter(converted_dict)
    for key, value in sorted_dict_to_value:
        print(key)