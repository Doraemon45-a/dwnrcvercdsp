#!/bin/bash

read -p "Masukkan URL MP4: " URL
read -p "Masukkan folder Google Drive: " DRIVE_PATH

mkdir -p downloads

FILENAME=$(basename "$URL")
FILEPATH="downloads/$FILENAME"

echo "Downloading..."

curl -L -o "$FILEPATH" "$URL"

SIZE=$(stat -c%s "$FILEPATH")
echo "Ukuran file: $SIZE bytes"

if [ "$SIZE" -lt 1000000 ]; then
  echo "File terlalu kecil, kemungkinan bukan file video."
  exit 1
fi

echo "Upload ke Google Drive..."

rclone copy "$FILEPATH" "gdrive:$DRIVE_PATH" --progress

echo "Selesai!"
