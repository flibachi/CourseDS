#!/bin/bash

input_file='../ex01/hh.csv'
output_file='../ex02/hh_sorted.csv'

if [ ! -f "$input_file" ]; then
    echo "Ошибка"
    echo "Файл '$input_file' не найден."
    exit 1
fi

{
    head -n 1 $input_file > $output_file;
    tail -n +2 $input_file | sort -t',' -k2,2 -k1,1
    } >> $output_file