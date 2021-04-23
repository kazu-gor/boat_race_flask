import requests
from bs4 import BeautifulSoup
import time
import fileinput

def scraping_program(date="2000-06-23", place=12):
    year, month, day = date.split("-")
    year_month = f"{year}{month}"
    file = f"data/{month}{day}.txt"
    with open(file, "a", encoding='utf-8') as f:
        try:
            url = f"http://www1.mbrace.or.jp/od2/B/{year_month}/{place}/{day}.html"
        except ValueError:
            return None, None, None

        response = requests.get(url)
        response.encoding = response.apparent_encoding

        bs = BeautifulSoup(response.text, "html.parser")


        for pre in bs.find_all("pre"):
            f.write(pre.text)
        time.sleep(1)
    return year, month, day

def edit_sentence(sen):
    s_list = sen.rstrip().split(" ")
    
    for i in range(16, 8, -2):
        s_list.insert(2, s_list[1][i-2:i])
    s_list.insert(2, s_list[1][4:8])
    s_list.insert(2, s_list[1][:4])
    del s_list[1]
    while True:
        try:
            s_list.remove("")
        except ValueError:
            break
    if len(s_list) > 15:
        del s_list[15: len(s_list)]
            
    return s_list

def edit_program(month, day):
    input_file = f"data/{month}{day}.txt"
    output_file = f"edited_data/{month}{day}.txt"
    results = []

    with open(input_file, "r", encoding='utf-8') as f:
        with open(output_file, "a", encoding="utf-8") as g:
            count = 0
            for row in f:
                column = row.rstrip().split("\n")

                if 2<= count <=7:
                    g.write(f"{edit_sentence(column[0])}\n")
                    results.append(edit_sentence(column[0]))
                    count += 1
                    if count >= 8:
                        count = 0

                if len(column[0]) == 79:
                    count += 1
    return results