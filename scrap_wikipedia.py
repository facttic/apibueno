import re
from bs4 import BeautifulSoup
import html
import requests

url = "https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina"
page = requests.get(url)


soup = BeautifulSoup(page.content, 'html.parser')

epidemiologia_table = soup.find('table', 'sortable')

estadisticas_table = soup.find_all('table', class_="wikitable")[1]


def sanitize_crappy_text(td):
    result = html.unescape((td.string or td.get_text()).strip())
    if td.a and not re.match(r"^#cite", td.find('a').get('href')):
        result = html.unescape(td.find('a').string.strip())
    # handle https://www.crummy.com/software/BeautifulSoup/bs4/doc/#output-formatters
    # remove brackets
    result = re.sub(r"\[(.*?)\]", "", result)
    # remove &nbsp;
    result = result.replace("\xa0", "")
    # remove zero width space
    result = result.replace("\u200b", "")
    # try to cast into int
    return cast_to_int(result)

def cast_to_int(val):
    try:
        return int(val)
    except Exception as e:
        return val

def process_table(table):
    rows = table.find_all('tr')[1:]
    headers = table.find('tr').find_all('th')
    rows_headers = list(map(lambda th: th.get_text(strip=True), headers))
    print(rows_headers)
    entries = []
    for row in rows:
        cells = row.find_all('td')

        if len(cells) > 1:
            entry = list(map(sanitize_crappy_text, cells))
            entries.append(entry)

    print(entries)
    return entries


process_table(epidemiologia_table)
print("====socotroco====")
process_table(estadisticas_table)
