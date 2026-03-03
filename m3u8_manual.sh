#!/bin/bash

echo "===== MULTI MANUAL M3U8 DOWNLOADER ====="
echo "Paste URL satu per baris."
echo "Ketik DONE jika selesai."
echo ""

mkdir -p downloads

LINKS=()

# Input multi link
while true; do
  read -p "M3U8: " URL
  if [[ "$URL" == "DONE" ]]; then
    break
  fi
  if [[ -n "$URL" ]]; then
    LINKS+=("$URL")
  fi
done

TOTAL=${#LINKS[@]}

if [ "$TOTAL" -eq 0 ]; then
  echo "Tidak ada link."
  exit 1
fi

echo ""
echo "Total link: $TOTAL"
echo ""

INDEX=1

for M3U8 in "${LINKS[@]}"; do

  echo "===== Downloading ($INDEX/$TOTAL) ====="

  OUTPUT="downloads/video_${INDEX}_$(date +%s).mp4"

  ffmpeg \
    -protocol_whitelist file,http,https,tcp,tls \
    -i "$M3U8" \
    -c copy \
    -bsf:a aac_adtstoasc \
    "$OUTPUT"

  if [ $? -eq 0 ]; then
    echo "✅ Selesai: $OUTPUT"
  else
    echo "❌ Gagal download untuk link ke-$INDEX"
  fi

  echo ""
  INDEX=$((INDEX+1))

done

echo "===== SEMUA PROSES SELESAI ====="