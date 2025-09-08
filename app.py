import os
import socket, time
import asyncio
import aiohttp

asciiart = '''  _  __                     _          _   _   _             _    
| |/ /__ _ _   _ _ __ __ _( )___     / \ | |_| |_ __ _  ___| | __
| ' // _` | | | | '__/ _` |// __|   / _ \| __| __/ _` |/ __| |/ /
| . \ (_| | |_| | | | (_| | \__ \  / ___ \ |_| || (_| | (__|   < 
|_|\_\__,_|\__, |_|  \__,_| |___/ /_/   \_\__|\__\__,_|\___|_|\_\
           |___/                                                 
 _____         _     _____           _ 
|_   _|__  ___| |_  |_   _|__   ___ | |
  | |/ _ \/ __| __|   | |/ _ \ / _ \| |
  | |  __/\__ \ |_    | | (_) | (_) | |
  |_|\___||___/\__|   |_|\___/ \___/|_|
'''

siteurl = "null"

def ping(host, port=80, timeout=2):
    start = time.time()
    try:
        s = socket.create_connection((host, port), timeout)
        latency = (time.time() - start) * 1000
        print(f"{host}:{port} ulaşıldı, gecikme: {latency:.2f} ms")
        s.close()
        return latency
    except Exception as e:
        print(f"{host}:{port} ulaşılamadı: {e} [BETA olması nedeniyle göz ardı edilebilir bir hata.]")
        return None

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    url = siteurl
    try:
        count = int(input("Kaç eşzamanlı istek gönderilsin? "))
    except ValueError:
        print("Lütfen bir sayı gir!")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for _ in range(count)]
        results = await asyncio.gather(*tasks)
        print(f"{len(results)} istek tamamlandı")

print(asciiart)

with open("tos.md", "r", encoding="utf-8") as f:
    print(f.read())

cevap = input("\nŞartları kabul ediyor musun? (y/n): ").strip().lower()

if cevap == "y":
    print("Devam ediliyor...")
    siteurl = input("Hedef sitenin adresini girin. (Örnek: https://example.domain): ").strip().lower()
    ping(siteurl)
    onay = input('"'+siteurl+'" '+"Bu adres doğru mu? (y/n): ")
    if onay == 'y':
        print("Onay verildi.\n")
        asyncio.run(main())
    elif onay == 'n':
        exit()
    else:
        print("Geçersiz cevap! Uygulamadan çıkılıyor")
        exit()
elif cevap == "n":
    print("Uygulama kapatılıyor...")
    exit()
else:
    print("Geçersiz giriş! Program sonlandırıldı.")
    exit()


