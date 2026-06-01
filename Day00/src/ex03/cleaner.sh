#!/bin/sh

input_file="../ex02/hh_sorted.csv"
output_file="hh_positions.csv"

if [ ! -f "$input_file" ]; then
    echo "Ошибка"
    echo "Файл '$input_file' не найден."
    exit 1
fi

head -n 1 "$input_file" > "$output_file"
tail -n +2 "$input_file" | awk -F ',' '
BEGIN {
    OFS = ",";
}
{
    id = $1
    created_at = $2
    name = $3
    has_test = $4
    alternate_url = $5

    cleaned_name = ""
    if (tolower(name) ~ /junior/) {
        cleaned_name = cleaned_name "Junior"
    }
    if (tolower(name) ~ /middle/) {
        cleaned_name = (cleaned_name == "" ? "" : cleaned_name "/") "Middle"
    }
    if (tolower(name) ~ /senior/) {
        cleaned_name = (cleaned_name == "" ? "" : cleaned_name "/") "Senior"
    }
    if (cleaned_name == "") {
        cleaned_name = "-"
    }
    
    print id, created_at, "\"" cleaned_name "\"", has_test, alternate_url
}
' >> "$output_file"

echo "Результат сохранен в файл $output_file"