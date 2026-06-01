#!/bin/sh

output_file="hh_combined.csv"

csv_files=$(ls *.csv 2>/dev/null | grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}\.csv$")
if [ -z "$csv_files" ]; then
  echo "Файлы не найдены"
  exit 1
fi

header=$(head -n 1 $(echo "$csv_files" | head -n 1))
echo "$header" > "$output_file"

for file in $csv_files; do
  tail -n +2 "$file" >> "$output_file"
done

echo "CSV файлы объединены в '$output_file'."