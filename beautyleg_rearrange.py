"""
Python version: 3.6.5
Library dependency:
- pip install Pillow
- pip install beautifulsoup4
"""

import re
import os
import webbrowser
from PIL import Image
from urllib.request import urlretrieve, urlopen
from bs4 import BeautifulSoup

def _menu():
    print("""Menu:
------------------------------
[1] Beautyleg Free Download
[2] Beautyleg Magazine
------------------------------""")
    sel = input("Please choose your option (Enter to leave): ")
    if sel == '1' or sel == '2':
        return int(sel)
    else:
        return None

def _parse_inp(sel):
    if sel == 1:
        album = input("Enter album no. (ex: 3) or range (ex: 2~12) (album no. must >= 1): ")
    if sel == 2:
        album = input("Enter album no. (ex: 3) or range (ex: 2~12) (album no. must >= 201): ")
    if album and re.search(r"^(-?\d+)$", album) or re.search(r"^(-?\d+)~(-?\d+)$", album):
        alb_range = re.split(r"~", album)
        if len(alb_range) > 1:
            start = int(alb_range[0])
            end = int(alb_range[1])
        else:
            start = end = int(alb_range[0])
        if sel == 1 and start < 1:
            print("Album no. must >= 1!")
            return None
        elif sel == 2 and start < 201:
            print("Album no. must >= 201!")
            return None
        else:
            return (start, end)
    else:
        print("Your input is not correct!")

def _search_jpg(album_no, sel):
    if sel == 1:
        url = urlopen("http://beautyleg.com/photo/show.php?no=" + str(album_no))
    elif sel == 2:
        url = urlopen("http://beautyleg.com/magazine/news_show.php?no=" + str(album_no))
    soup = BeautifulSoup(url, 'html.parser')
    return [
        link.get('href')
        for link in soup.find_all('a')
        if re.search(r'jpg', link.get('href'))
    ]

def _dir_path(num, sel):
    if sel == 1:
        return "./bl_" + str(num)
    elif sel == 2:
        return "./mag_" + str(num)

def _html_path(num, sel):
    if sel == 1:
        return "bl_" + str(num) + ".html"
    elif sel == 2:
        return "mag_" + str(num) + ".html"

def _download(fn, url, no, sel):
    if sel == 1:
        full_fn = "./bl_" + str(no) + "/" + fn
    if sel == 2:
        url = "http://beautyleg.com/magazine" + url[1:]
        full_fn = "./mag_" + str(no) + "/" + fn
    urlretrieve(url, filename=full_fn)
    return full_fn

def main():
    select = _menu()
    if select:
        inp = _parse_inp(select)
        if inp:
            num1, num2 = inp
            while num1 <= num2:
                wide = []
                narrow = []
                jpg = _search_jpg(num1, select)
                path = _dir_path(num1, select)
                if not os.path.isdir(path):
                    os.mkdir(path)
                print(f"There are {len(jpg)} files in the album {num1}!")
                re_jpg = re.compile(r"\d{4}.jpg")
                for img in jpg:
                    re_img = re_jpg.search(img)
                    fn = re_img.group(0)
                    full_fn = _download(fn, img, num1, select)
                    print(f"{fn}...done!")
                    with Image.open(full_fn) as j:
                        w, h = j.size
                        if w > h:
                            wide.append(full_fn)
                        else:
                            narrow.append(full_fn)
                html_path = _html_path(num1, select)
                with open(html_path, "w") as fout:
                    fout.write("""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
""")
                    for item in narrow:
                        fout.write(f'<img src="{item}" width="50%">')
                    for item in wide:
                        fout.write(f'<img src="{item}" width="100%">')
                    fout.write("""
</body>
</html>""")
                num1 += 1

main()
