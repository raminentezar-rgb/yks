import urllib.request
import re
import os

os.makedirs('static/images', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

urls_to_try = [
    'https://tr.wikipedia.org/wiki/Avrasya_%C3%9Cniversitesi',
    'https://logowik.com/avrasya-universitesi-logo-vector-15777.html',
    'https://www.avrasya.edu.tr'
]

logo_url = None
for u in urls_to_try:
    try:
        req = urllib.request.Request(u, headers=headers)
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'https?://[^\s\"\'<>]+(?:logo|avrasya)[^\s\"\'<>]+\.(?:png|jpg|svg|jpeg)', html, re.I)
        for m in matches:
            if 'png' in m.lower() or 'logo' in m.lower():
                logo_url = m
                print("Found logo candidate:", logo_url)
                break
        if logo_url: break
    except Exception as e:
        print("Error fetching", u, e)

if logo_url:
    try:
        req = urllib.request.Request(logo_url, headers=headers)
        data = urllib.request.urlopen(req, timeout=5).read()
        with open('static/images/avrasya_logo.png', 'wb') as f:
            f.write(data)
        print("Successfully downloaded logo to static/images/avrasya_logo.png (" + str(len(data)) + " bytes)")
    except Exception as e:
        print("Error downloading logo image:", e)
else:
    print("No logo URL found.")
