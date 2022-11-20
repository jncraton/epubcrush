import urllib.request 
import os
import epubcrush
import subprocess

urls = [
 "https://standardebooks.org/ebooks/karl-marx_friedrich-engels/the-communist-manifesto/samuel-moore/downloads/karl-marx_friedrich-engels_the-communist-manifesto_samuel-moore.epub",
 "https://www.gutenberg.org/cache/epub/41/pg41-images-3.epub",
]

print('| File | Original | Crushed | txt | txtz |')

for i, url in enumerate(urls):
    filename, headers = urllib.request.urlretrieve(url)
    original_size = os.stat(filename).st_size / 1000

    filename_txt = filename+'.txt'
    subprocess.run(['pandoc', '--read', 'epub', filename, '--write', 'plain', '-o', filename_txt])
    txt_size = os.stat(filename_txt).st_size // 1000

    filename_txtz = filename+'.txtz'
    subprocess.run(['advzip', '--add', filename_txtz, filename_txt])
    txtz_size = os.stat(filename_txtz).st_size // 1000

    epubcrush.crush_epub(filename)
    new_size = os.stat(filename).st_size / 1000
    #print(original_size, new_size, new_size/original_size, txt_size, txtz_size)

    print(f'| {i+1:4} | {original_size:8} | {new_size:7} | {txt_size:3} | {txtz_size:4} |') 
