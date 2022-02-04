#!/bin/bash

while getopts ":n:k:m:f:" opt; do
  case $opt in
    n) params="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done
IFS="; " read -r -a array <<< "$params"
bucket_name="${array[0]}"
key="${array[1]}"
mode="${array[2]}"
frames="${array[3]}"
printf "Bucket name is %s\n" "$bucket_name"
printf "Key is %s\n" "$key"
printf "Mode is %s\n" "$mode"
printf "Frames quotient is %s\n" "$frames"

python "/download_from_bucket.py" -n\
"$bucket_name" -k "$key"
key_without_end="${key:0:29}"
echo $key_without_end
ffmpeg -an -i $key -vcodec libx264 -pix_fmt yuv420p -profile:v baseline -level 3 "${key_without_end}.mp4"
python "/upload_to_bucket.py" -n\
"$bucket_name" -b "${key_without_end}.mp4"

python "/main.py" -v "${key_without_end}.mp4" -m "$mode" -o "$key_without_end" -f $frames

if [ "$mode" = "check" ]; then
    python "/upload_to_bucket.py" -n\
    "$bucket_name" -b "${key_without_end}_inference.mp4"
    rm "${key_without_end}_inference.mp4"
else
    python "/upload_to_bucket.py" -n\
    "$bucket_name" -b "/${key_without_end}"
    rm -rf "$key_without_end"
    fi
rm "$key"
rm "${key_without_end}.mp4"
