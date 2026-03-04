from telethon import TelegramClient
from telethon.errors import FloodWaitError
from tqdm import tqdm
import os
import asyncio

api_id = 1916950
api_hash = "9e268fee501ad809e4f5f598adcb970c"

client = TelegramClient("mysession", api_id, api_hash)


async def upload_file(target, file_path, index, total):

    file_size = os.path.getsize(file_path)

    print(f"\nUploading ({index}/{total}): {os.path.basename(file_path)}")

    with tqdm(
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=os.path.basename(file_path),
    ) as pbar:

        async def progress(current, total):
            pbar.total = total
            pbar.update(current - pbar.n)

        while True:
            try:

                await client.send_file(
                    target,
                    file_path,
                    supports_streaming=True,
                    workers=6,
                    progress_callback=progress
                )

                break

            except FloodWaitError as e:

                wait = int(e.seconds)

                print(f"\n⚠ FloodWait {wait} detik. Menunggu...")

                await asyncio.sleep(wait)

            except Exception as e:

                print(f"\n❌ Error upload {file_path}: {e}")

                break


async def main():

    print("\n=== Telegram Upload Menu ===\n")
    print("1. Cowok")
    print("2. Cewek")
    print("3. Diri sendiri")
    print("4. Custom\n")

    choice = input("Pilih tujuan (1-4): ").strip()

    if choice == "1":
        target_input = "https://t.me/+UMMnQy0_eUJlNjI1"

    elif choice == "2":
        target_input = "https://t.me/+-b0j641W63gzNDVl"

    elif choice == "3":
        target_input = "me"

    elif choice == "4":
        target_input = input("Masukkan username / link: ")

    else:
        print("Pilihan tidak valid")
        return

    print("\nResolving target...")

    target = await client.get_entity(target_input)

    folder = input("\nMasukkan path folder: ")

    if not os.path.isdir(folder):
        print("Folder tidak ditemukan")
        return

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]

    if not files:
        print("Tidak ada file")
        return

    total = len(files)

    print(f"\nTotal file ditemukan: {total}")

    for i, file in enumerate(files, start=1):

        await upload_file(target, file, i, total)

    print("\n✅ Semua upload selesai")


with client:
    client.loop.run_until_complete(main())