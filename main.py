import bs4
import requests
from bs4 import BeautifulSoup

HTMLBOOK_URL = "https://htmlbook.ru"
tags = dict()


def get_tags():
    r = requests.get(HTMLBOOK_URL)
    soup = BeautifulSoup(r.text, "lxml")
    m = soup.find("div", id="block-menu-html")
    for i in m.findAll("a"):
        if i.get_text()[0] != "<" or i.get_text()[0:2] == "<!":
            continue
        tags[i.get_text()[1:-1]] = HTMLBOOK_URL + i["href"]

    print(tags)


def fetch_and_show_tag_info(tag):
    print(f"Это тэг {tag}, {tags[tag]}")

    r = requests.get(tags[tag])
    soup = BeautifulSoup(r.text, "lxml")
    paragraphs = []
    description = ""
    attributes = ""
    for i in soup.findAll("h3"):
        if "Описание" not in i.get_text():
            continue
        disk = i

        next_sib = disk.next_sibling
        while next_sib:
            if next_sib.name is None:
                next_sib = next_sib.next_sibling
                continue
            if next_sib.name == "p":
                paragraphs.append(next_sib)
                next_sib = next_sib.next_sibling
                continue
            break

    for i in soup.findAll("h3"):
        if "Атрибуты" not in i.get_text():
            continue
        disk = i

        next_sib = disk.next_sibling
        while next_sib:
            if next_sib.name is None:
                next_sib = next_sib.next_sibling
                continue
            if next_sib.name == "dl":
                data = []
                for i in next_sib.children:
                    if i.text == "\n":
                        continue
                    data.append(i.text)

                if data:
                    attributes = "Атрибуты: \n"
                for i in range(0, len(data), 2):
                    attributes += "    " + data[i] + ": " + data[i+1] + "\n"
                next_sib = next_sib.next_sibling
                continue
            break


    for i in paragraphs:
        description += " ".join([i for i in i.stripped_strings]) + "\n"

    print(description)
    print(attributes)


def work_with_user():
    t = input("Введите название тега: ")
    if t == "/quit":
        return 0
    if t in tags:
        fetch_and_show_tag_info(t)
    else:
        print("Такой тэг не найден")
    return 1


if __name__ == '__main__':
    get_tags()
    #fetch_and_show_tag_info("a")




    while work_with_user():
        pass
