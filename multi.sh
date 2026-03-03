#!/bin/bash

echo "===== MULTI MP4 DOWNLOADER ====="
echo "Masukkan URL satu per baris."
echo "Jika sudah selesai, ketik: DONE"
echo ""

mkdir -p downloads
URLS=()

# Input multiple URL
while true; do
  read -p "URL: " INPUT
  if [ "$INPUT" = "DONE" ]; then
    break
  fi
  URLS+=("$INPUT")
done

echo ""
echo "Total URL: ${#URLS[@]}"
echo "Mulai download..."
echo ""

# Download satu per satu
for URL in "${URLS[@]}"; do
  FILENAME=$(basename "$URL")
  FILEPATH="downloads/$FILENAME"

  echo "Downloading $FILENAME ..."

  curl -L \
    -H "User-Agent: Mozilla/5.0" \
    -o "$FILEPATH" \
    "$URL"

  if [ -f "$FILEPATH" ]; then
    SIZE=$(stat -c%s "$FILEPATH")
  else
    SIZE=0
  fi

  echo "Ukuran: $SIZE bytes"

  if [ "$SIZE" -lt 1000000 ]; then
    echo "⚠ File terlalu kecil, kemungkinan gagal."
  else
    echo "✅ Sukses download $FILENAME"
  fi

  echo "---------------------------------"
done

echo ""
echo "Semua download selesai."

# Tanya apakah mau upload
read -p "Upload semua file ke Google Drive sekarang? (y/n): " CONFIRM

if [ "$CONFIRM" = "y" ]; then
  read -p "Masukkan folder tujuan Google Drive: " DRIVE_PATH

  echo "Upload dimulai..."

  rclone copy downloads/ "gdrive:$DRIVE_PATH" --progress

  echo "✅ Semua file berhasil diupload."
else
  echo "Upload dibatalkan."
fi

echo "===== SELESAI ====="
