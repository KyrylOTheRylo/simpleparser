from bs4 import BeautifulSoup
import csv
import requests
import csv

FIlENAME = "Output.csv"
HOME = "https://baza-gai.com.ua"
URL = "https://baza-gai.com.ua/catalog/renault/kadjar"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"
}


def get_html(url, params=''):
    re = requests.get(url, headers=HEADERS, params=params)
    return re


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find("tbody").find_all("tr")
    vehicle = []
    for item in items:
        vehicle.append(
            {
                "td": item.find('td').get_text(),
                "link": HOME + item.find('td').find('a').get("href"),
                "params": (item.find_all('td')[3].get_text()),
                "year": (item.find_all('td')[1].get_text())

            }

        )

    return vehicle


def save_doc(items, path):
    with open(path, "w", newline='',encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["td", "link", "params", "year"])
        for item in items:
            writer.writerow([item["td"], item["link"], item["params"], item["year"]])


def parser():
    try:
        PAGENATION = int(input("Amount of pages: ").strip())
        html = get_html(URL)
        if html.status_code == 200:
            cards = []
            for page in range(1, PAGENATION + 1):
                print(f'Parsing the page {page}')
                html = get_html(URL, params={"page": page})
                cards.extend(get_content(html.text))

        else:
            raise BaseException
    except BaseException:
        print("Something went wrong")
    return cards


save_doc(parser(), FIlENAME)
