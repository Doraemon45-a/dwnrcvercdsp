import requests
import os

headers = {
    "user-agent": "Mozilla/5.0",
    "referer": "https://x.com/"
}

# buat folder download
os.makedirs("images", exist_ok=True)


def download_from_tweet(tweet_url):

    api = tweet_url.replace("x.com", "api.vxtwitter.com")

    try:
        r = requests.get(api, headers=headers)

        if r.status_code != 200:
            print("Request gagal:", tweet_url)
            return

        data = r.json()

        if "media_extended" not in data:
            print("Tidak ada gambar:", tweet_url)
            return

        for m in data["media_extended"]:

            if m["type"] == "image":

                url = m["url"] + "?name=orig"

                # ambil nama file dari URL (sudah ada .jpg)
                filename = f"images/{m['url'].split('/')[-1]}"

                # skip jika file sudah ada
                if os.path.exists(filename):
                    print("Skip (sudah ada):", filename)
                    continue

                img = requests.get(url, headers=headers).content

                with open(filename, "wb") as f:
                    f.write(img)

                print("Downloaded:", filename)

    except Exception as e:
        print("Error:", e)


print("=== X Image Downloader ===\n")

print("1. Download dari 1 URL")
print("2. Download dari banyak URL\n")

choice = input("Pilih menu (1/2): ").strip()


if choice == "1":

    tweet_url = input("\nMasukkan URL post X: ").strip()

    download_from_tweet(tweet_url)


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
        download_from_tweet(url)

else:
    print("Pilihan tidak valid")