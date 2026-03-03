import re
import requests
import subprocess
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_tweet_id(url):
    match = re.search(r"status/(\d+)", url)
    return match.group(1) if match else None

def find_m3u8_from_html(url):
    r = requests.get(url, headers=HEADERS)
    html = r.text

    m3u8_matches = re.findall(r"https://video\.twimg\.com/[^\"']+\.m3u8[^\"']*", html)

    if not m3u8_matches:
        return None

    return m3u8_matches[0]

def choose_best_stream(master_m3u8):
    r = requests.get(master_m3u8, headers=HEADERS)
    lines = r.text.splitlines()

    best_url = None
    best_bandwidth = 0

    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            bandwidth_match = re.search(r"BANDWIDTH=(\d+)", line)
            if bandwidth_match:
                bandwidth = int(bandwidth_match.group(1))
                stream_url = lines[i+1]

                if bandwidth > best_bandwidth:
                    best_bandwidth = bandwidth
                    best_url = stream_url

    if best_url and not best_url.startswith("http"):
        base = master_m3u8.rsplit("/", 1)[0]
        best_url = base + "/" + best_url

    return best_url

def download_stream(m3u8_url):
    os.makedirs("downloads", exist_ok=True)
    output = "downloads/output.mp4"

    subprocess.run([
        "ffmpeg",
        "-protocol_whitelist", "file,http,https,tcp,tls",
        "-i", m3u8_url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output
    ])

    print("\nDownload selesai:", output)

if __name__ == "__main__":
    tweet_url = input("Masukkan link X.com: ")

    tweet_id = extract_tweet_id(tweet_url)
    if not tweet_id:
        print("Link tidak valid.")
        exit()

    print("Tweet ID:", tweet_id)

    master_m3u8 = find_m3u8_from_html(tweet_url)

    if not master_m3u8:
        print("Tidak ditemukan m3u8.")
        exit()

    print("Master m3u8 ditemukan:")
    print(master_m3u8)

    best_stream = choose_best_stream(master_m3u8)

    if not best_stream:
        print("Gagal memilih kualitas terbaik.")
        exit()

    print("Kualitas tertinggi:")
    print(best_stream)

    download_stream(best_stream)