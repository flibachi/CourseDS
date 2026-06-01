#!/bin/bash

input_file='../ex00/hh.json'
output_file='hh.csv'

if [ ! -f "$input_file" ]; then
    echo "Ошибка"
    echo "Файл '$input_file' не найден."
    exit 1
fi

{
    echo "“id“", "“created_at“", "“name“", "“has_test“", "“alternate_url“"
    jq -r -f filter.jq $input_file
} > $output_file

echo "Результат сохранен в файл $output_file"