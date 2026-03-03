from telethon import TelegramClient
from tqdm import tqdm
import os

api_id = 1916950            # GANTI
api_hash = "9e268fee501ad809e4f5f598adcb970c" # GANTI

client = TelegramClient("mysession", api_id, api_hash)

async def main():
    target = input("Kirim ke (me / @channel / username): ")
    file_path = input("Masukkan path file: ")

    if not os.path.exists(file_path):
        print("File tidak ditemukan.")
        return

    file_size = os.path.getsize(file_path)

    print("Uploading...\n")

    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:

        async def progress_callback(current, total):
            pbar.total = total
            pbar.update(current - pbar.n)

        await client.send_file(
            target,
            file_path,
            supports_streaming=True,
            progress_callback=progress_callback
        )

    print("\nUpload selesai!")

with client:
    client.loop.run_until_complete(main())