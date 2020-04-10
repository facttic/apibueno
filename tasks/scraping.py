import re
from bs4 import BeautifulSoup
import html
import requests

class Scraping:
    def __init__(self):
        self.URL = "https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina"
        self.page = requests.get(self.URL)
        soup = BeautifulSoup(self.page.content, 'html.parser')
        self.epidemiologia_table = soup.find('table', 'sortable')
        self.estadisticas_table = soup.find_all('table', class_="wikitable")[1]
        self.process()

    def sanitize_crappy_text(self, td):
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
        return self.cast_to_int(result)

    def cast_to_int(self, val):
        try:
            return int(val)
        except Exception as e:
            return val

    def process_table(self, table):
        rows = table.find_all('tr')[1:]
        headers = table.find('tr').find_all('th')
        rows_headers = list(map(lambda th: th.get_text(strip=True), headers))
        print(rows_headers)
        entries = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                entry = list(map(self.sanitize_crappy_text, cells))
                entries.append(entry)

        print(entries)
        return entries

    def process(self):
        self.process_table(self.epidemiologia_table)
        print("====socotroco====")
        self.process_table(self.estadisticas_table)

if __name__ == "__main__":
    Scraping()
