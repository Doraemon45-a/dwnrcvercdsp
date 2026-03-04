import requests
import subprocess
import os

headers = {
    "user-agent": "Mozilla/5.0",
    "referer": "https://x.com/"
}

# buat folder video
os.makedirs("videos", exist_ok=True)


def download_video(tweet_url):

    api = tweet_url.replace("x.com", "api.vxtwitter.com")

    try:
        r = requests.get(api, headers=headers)

        if r.status_code != 200:
            print("Request gagal:", tweet_url)
            return

        data = r.json()

        if "media_extended" not in data:
            print("Tidak ada video:", tweet_url)
            return

        for m in data["media_extended"]:

            if m["type"] == "video":

                m3u8_url = m["url"]

                video_id = m3u8_url.split("/")[-1].split(".")[0]

                filename = f"videos/{video_id}.mp4"

                # skip jika sudah ada
                if os.path.exists(filename):
                    print("Skip (sudah ada):", filename)
                    continue

                print("\nStream URL:")
                print(m3u8_url)

                print("Downloading:", filename)

                subprocess.run([
                    "ffmpeg",
                    "-loglevel", "error",
                    "-y",
                    "-i", m3u8_url,
                    "-c", "copy",
                    filename
                ])

                print("Selesai:", filename)

    except Exception as e:
        print("Error:", e)


print("=== X Video Downloader ===\n")

print("1. Download dari 1 URL")
print("2. Download dari banyak URL\n")

choice = input("Pilih menu (1/2): ").strip()


if choice == "1":

    tweet_url = input("\nMasukkan URL post X: ").strip()

    download_video(tweet_url)


elif choice == "2":

    print("\nMasukkan banyak URL (ketik 'done' untuk mulai download)\n")

    urls = []

    while True:

        u = input("URL: ").strip()

        if u.lower() == "done":
            break

        if u:
            urls.append(u)

    print("\nMulai download...\n")

    for url in urls:
        download_video(url)

else:
    print("Pilihan tidak valid")