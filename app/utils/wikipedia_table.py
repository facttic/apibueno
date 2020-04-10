"""app.utils.wikipedia_table.py"""
import logging
import re
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)

def sanitize_crappy_text(item):
    item = re.sub(r"\[(.*?)\]", "", item)
    # remove &nbsp;
    item = item.replace("\xa0", "")
    item = item.replace(" ", "")
    # remove zero width space
    item = item.replace("\u200b", "")
    return cast_to_int(item)

def cast_to_int(val):
    try:
        return int(val)
    except Exception as e:
        return val

def parse_table(html, table={'class':'wikitable'}, order=0):
    data = []
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all('table', table)[order]
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # Just sanitize numbers
        cols = map( lambda i:  sanitize_crappy_text(i[1]) if i[0] > 0 else i[1], enumerate(cols) )
        cols = [ele for ele in cols]
        if cols:
            data.append(cols)
    return data

