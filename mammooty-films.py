import os
import csv

import requests
from bs4 import BeautifulSoup

URL = "http://mammootty.com/movies"
output_name = "filmography"


def scrape(url, output_name):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content)
    table_classes = {"class": ["wikitables", "sortable", "plainrowheader"]}
    tables = soup.findAll("table", table_classes)

    try:
        os.mkdir(output_name)
    except Exception:
        pass

    for index, table in enumerate(tables):
        if index == 0:
            filename = output_name
        else:
            filename = output_name + '_' + str(index)

        filepath = os.path.join(output_name, filename) + '.csv'

        with open(filepath, mode='w', newline='', encoding='utf-8') as output:
            csv_writer = csv.writer(output, quoting=csv.QUOTE_ALL)

            write_html_table_to_csv(table, csv_writer)


def write_html_table_to_csv(table, writer):
    saved_rowspans = []
    for row in table.findAll("tr"):
        cells = row.findAll(["th", "td"])
        if cells:
            cleaned = clean_data(cells)
            writer.writerow(cleaned)


def clean_data(row):
    cleaned_cells = []
    for cell in row:
        references = cell.findAll("sup", {"class": "reference" })
        if references:
            for ref in references:
                ref.extract()

        sortkeys = cell.findAll("span", {"class": "sortkey"})
        if sortkeys:
            for ref in sortkeys:
                ref.extract()

        text_items = cell.findAll(text=True)
        no_footnotes = [text for text in text_items if text[0] != '[']

        cleaned = (
                ''.join(no_footnotes)
                .replace('\xa0', ' ')
                .replace('\n', ' ')
                .strip()
                )

        cleaned_cells += [cleaned]

    return cleaned_cells


scrape(URL, output_name)
