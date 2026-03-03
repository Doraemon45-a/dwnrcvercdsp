from telethon import TelegramClient
from tqdm import tqdm
import os
import asyncio

api_id = 1916950          # GANTI
api_hash = "9e268fee501ad809e4f5f598adcb970c"    # GANTI

client = TelegramClient("mysession", api_id, api_hash)

async def upload_file(target, file_path, index, total_files):
    file_size = os.path.getsize(file_path)

    print(f"\nUploading ({index}/{total_files}): {os.path.basename(file_path)}")

    with tqdm(
        total=file_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc=os.path.basename(file_path),
    ) as pbar:

        async def progress_callback(current, total):
            pbar.total = total
            pbar.update(current - pbar.n)

        await client.send_file(
            target,
            file_path,
            supports_streaming=True,
            progress_callback=progress_callback
        )

async def main():
    target = input("Kirim ke (me / @channel / username): ")
    folder_path = input("Masukkan path folder (contoh: downloads): ")

    if not os.path.isdir(folder_path):
        print("Folder tidak ditemukan.")
        return

    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    if not files:
        print("Tidak ada file dalam folder.")
        return

    print(f"\nTotal file ditemukan: {len(files)}")

    for idx, file_path in enumerate(files, start=1):
        await upload_file(target, file_path, idx, len(files))

    print("\n✅ Semua upload selesai!")

with client:
    client.loop.run_until_complete(main())