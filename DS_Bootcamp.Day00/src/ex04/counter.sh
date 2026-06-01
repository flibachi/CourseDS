#!/bin/sh

input_file="../ex03/hh_positions.csv"
output_file="hh_uniq_positions.csv"

if [ ! -f "$input_file" ]; then
    echo "Ошибка"
    echo "Файл '$input_file' не найден."
    exit 1
fi

{
    echo "\"name\",\"count\""
    tail -n +2 "$input_file" |
    awk -F ',' '{
        gsub(/"/, "", $3);
        gsub(/^[ \t]+|[ \t]+$/, "", $3);
        if ($3 == "-") next; 
        else print $3 
    }' |
    tr -d '"' |
    sort |
    uniq -c |
    sort -r -n |
    awk '{print "\"" $2 "\"," $1}'
} > "$output_file"

echo "Результат сохранен в файл $output_file"