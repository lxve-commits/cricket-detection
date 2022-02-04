#!/bin/bash

while getopts ":n:k:m:f:" opt; do
  case $opt in
    n) params="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
IFS=', ' read -r -a array <<< "$params"
bucket_name="${array[0]}"
key="${array[1]}"
mode="${array[2]}"
frames="${array[3]}"
printf "Bucket name is %s\n" "$bucket_name"
printf "Key is %s\n" "$key"
printf "Mode is %s\n" "$mode"
printf "Frames quotient is %s\n" "$frames"
