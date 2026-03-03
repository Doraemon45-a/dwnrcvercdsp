#!/bin/bash

echo "===== HARDCORE SMART DOWNLOADER (Codespace Edition) ====="

read -p "Masukkan direct file URL: " URL
read -p "Masukkan folder Google Drive tujuan: " DRIVE_PATH

mkdir -p downloads

FILENAME=$(basename "$URL")
FILEPATH="downloads/$FILENAME"

# ==========================
# Auto detect qu.ax referer
# ==========================
REFERER=""
if [[ "$URL" == *"qu.ax/x/"* ]]; then
  ID=$(basename "$URL" .mp4)
  REFERER="https://qu.ax/$ID"
  echo "Detected qu.ax link"
  echo "Auto Referer: $REFERER"
fi

echo ""
echo "Attempt 1: aria2 multi-connection..."

aria2c \
  -x 16 -s 16 -k 1M \
  --header="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/145.0 Safari/537.36" \
  --header="Accept: */*" \
  --header="Referer: $REFERER" \
  --file-allocation=none \
  -d downloads \
  -o "$FILENAME" \
  "$URL"

if [ -f "$FILEPATH" ]; then
  SIZE=$(stat -c%s "$FILEPATH")
else
  SIZE=0
fi

echo "Downloaded size: $SIZE bytes"

# ==========================
# Fallback jika kecil
# ==========================
if [ "$SIZE" -lt 1000000 ]; then
  echo "Fallback to CURL..."

  curl -L \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
    -H "Accept: */*" \
    -H "Referer: $REFERER" \
    -o "$FILEPATH" \
    "$URL"

  SIZE=$(stat -c%s "$FILEPATH")
  echo "New size: $SIZE bytes"
fi

# ==========================
# Validasi akhir
# ==========================
if [ "$SIZE" -lt 1000000 ]; then
  echo "ERROR: File masih terlalu kecil. Kemungkinan IP diblok."
  exit 1
fi

echo ""
echo "Download berhasil!"

echo ""
read -p "Upload ke Google Drive sekarang? (y/n): " CONFIRM
CONFIRM=$(echo "$CONFIRM" | tr '[:upper:]' '[:lower:]')

if [ "$CONFIRM" = "y" ]; then
  echo "Upload dimulai..."
  rclone copy "$FILEPATH" "gdrive:$DRIVE_PATH" --progress
  echo "Upload selesai!"
else
  echo "Upload dibatalkan."
fi

echo "===== SELESAI ====="
