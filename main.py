from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
from collections import defaultdict

FOUNDING_YEAR = 1912


def generates_word_form(winery_age):
    if winery_age % 100 in [11, 12, 13, 14]:
        word_form = 'лет'
    elif winery_age % 10 == 1:
        word_form = 'год'
    elif winery_age % 10 in [2, 3, 4]:
        word_form = 'года'
    else:
        word_form = 'лет'
    return word_form


def main():
    now_time = datetime.datetime.now()
    winery_age = now_time.year - FOUNDING_YEAR
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    wines = pd.read_excel('wine.xlsx', na_values='nan', keep_default_na=False)
    wines_dict = wines.to_dict(orient='records')
    wines_categories = defaultdict(list)

    for wine in wines_dict:
        wine_category = list(wine.keys())[0]
        wines_categories[wine[wine_category]].append(wine)

    template = env.get_template('template.html')
    rendered_page = template.render(
        age_now=f"Уже {winery_age} {generates_word_form(winery_age)} с нами",
        wines=wines_categories
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
