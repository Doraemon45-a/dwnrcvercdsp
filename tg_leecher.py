import os
import requests
from tqdm import tqdm

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def upload_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    file_size = os.path.getsize(file_path)
    
    with open(file_path, "rb") as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading") as pbar:
            def progress_monitor(monitor):
                pbar.update(monitor.bytes_read - pbar.n)
            
            files = {
                "document": (os.path.basename(file_path), f)
            }
            data = {
                "chat_id": CHAT_ID
            }
            response = requests.post(url, data=data, files=files)
    
    print("Upload response:", response.json())

def download_file(url):
    os.system(f'aria2c -x 16 -s 16 -k 1M "{url}"')
    filename = url.split("/")[-1]
    return filename

if __name__ == "__main__":
    file_url = input("Masukkan direct file URL: ")
    
    filename = download_file(file_url)
    
    if os.path.exists(filename):
        print("Download selesai.")
        upload_to_telegram(filename)
    else:
        print("Download gagal.")