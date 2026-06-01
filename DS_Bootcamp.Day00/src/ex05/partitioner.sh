#!/bin/sh

input_file="../ex03/hh_positions.csv"
output_file="hh_uniq_positions.csv"

if [ ! -f "$input_file" ]; then
    echo "Ошибка"
    echo "Файл '$input_file' не найден."
    exit 1
fi

header=$(head -n 1 "$input_file")

tail -n +2 "$input_file" |
while IFS=',' read -r id created_at name has_test alternate_url; do
    date=$(echo "$created_at" | cut -d'T' -f1 | tr -d '"')
    if [ -n "$date" ]; then
        if [ ! -f "${date}.csv" ]; then
            echo "$header" > "${date}.csv"
        fi
        echo "$id,$created_at,$name,$has_test,$alternate_url" >> "${date}.csv"
    fi
done

echo "Данные разбиты по датам в файлы"