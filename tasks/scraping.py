import re
import html
import requests

import sys
sys.path.insert(0, "./app/utils")

from wikipedia_table import parse_table

class Scraping:
    def __init__(self):
        self.URL = "https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina"
        self.html = requests.get(self.URL).text
        self.process()

    def process(self):
        self.epidemiologia_table = parse_table(self.html, order=0)
        self.estadisticas_table = parse_table(self.html, order=1)
        self.mergeCsv()

    def mergeCsv(self):
        print(self.epidemiologia_table)
        print("====socotroco====")
        print(self.estadisticas_table)

if __name__ == "__main__":
    Scraping()
