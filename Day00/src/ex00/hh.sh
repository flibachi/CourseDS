#!/bin/bash

vacancy="data+scientist"
output_file="hh.json"

api="https://api.hh.ru/vacancies?per_page=20&page=0&text=$vacancy"

curl -s "$api" | jq '.' > hh.json

echo "Результат сохранен в файл $output_file"