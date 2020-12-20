import re
import bs4
import requests
import os


os.makedirs('./outFiles', exist_ok=True)

print("Downloading page https://developer.android.com/reference/android/app/package-summary...")
source = requests.get(
    "https://developer.android.com/reference/android/app/package-summary")
src = source.content
soup = bs4.BeautifulSoup(src, "lxml")

links = []
for td_tag in soup.find_all('td', class_='jd-linkcol'):
    a_tag = td_tag.find('a')
    links.append("https://developer.android.com" + a_tag.get('href'))


def getCautionNotes(id):
    global api
    result = soup.find(id=id)
    if result is not None:
        while True:
            result = result.nextSibling.nextSibling
            try:
                tag = result.name
            except:
                tag = ""
            if tag == "div":

                if result.find('p', class_="caution") is not None:
                    string = result.find('p', class_="caution").text
                    string = re.sub(r"\s+", " ", string)

                    with open('./outFiles2/' + api + '.txt', 'a+') as f:
                        f.write(result.find(
                            class_="api-name").text + ":" + string + '\n')
            else:
                break


for l in links:
    source = requests.get(l)
    print("Downloading page ", l, "...")
    src = source.content
    soup = bs4.BeautifulSoup(src, "lxml")
    api = soup.find('h1', class_='api-title').text
    getCautionNotes('fields_1')
    getCautionNotes('constants_1')
    getCautionNotes('public-methods_1')
    getCautionNotes('protected-methods_1')
