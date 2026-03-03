#!/bin/bash

echo "===== MANUAL M3U8 DOWNLOADER ====="
read -p "Paste URL m3u8: " M3U8

mkdir -p downloads

OUTPUT="downloads/video_$(date +%s).mp4"

echo ""
echo "Downloading..."
echo ""

ffmpeg \
  -protocol_whitelist file,http,https,tcp,tls \
  -i "$M3U8" \
  -c copy \
  -bsf:a aac_adtstoasc \
  "$OUTPUT"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Selesai:"
  echo "$OUTPUT"
else
  echo ""
  echo "❌ Gagal download."
fi
