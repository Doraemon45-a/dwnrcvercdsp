#!/bin/bash

echo "==== HARDCORE SMART DOWNLOADER (Codespace Edition) ===="

read -p "Masukkan direct file URL: " URL
read -p "Masukkan Referer (contoh: https://qu.ax/xxxxx): " REFERER
read -p "Masukkan folder Google Drive tujuan: " DRIVE_PATH

mkdir -p downloads

FILENAME=$(basename "$URL")
FILEPATH="downloads/$FILENAME"

echo "Installing rclone config..."
mkdir -p ~/.config/rclone

echo "Paste isi rclone.conf sekarang lalu tekan CTRL+D:"
cat > ~/.config/rclone/rclone.conf

echo "Attempt 1: aria2 (IDM style)..."

aria2c \
  -x 16 -s 16 -k 1M \
  --header="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/145.0 Safari/537.36" \
  --header="Referer: $REFERER" \
  -d downloads \
  -o "$FILENAME" \
  "$URL"

if [ -f "$FILEPATH" ]; then
  SIZE=$(stat -c%s "$FILEPATH")
else
  SIZE=0
fi

echo "Downloaded size: $SIZE bytes"

if [ "$SIZE" -lt 1000000 ]; then
  echo "File terlalu kecil. Fallback ke CURL..."

  curl -L \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
    -H "Referer: $REFERER" \
    -o "$FILEPATH" \
    "$URL"

  SIZE=$(stat -c%s "$FILEPATH")
  echo "New size: $SIZE bytes"
fi

if [ "$SIZE" -lt 1000000 ]; then
  echo "ERROR: File masih terlalu kecil. Kemungkinan diblok."
  exit 1
fi

echo "Upload ke Google Drive..."

rclone copy "$FILEPATH" "gdrive:$DRIVE_PATH" --progress

echo "Selesai!"