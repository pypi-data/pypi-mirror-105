# pip_search.py

from rich.console import Console
from rich.table import Table
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests


def search(query):
    api_url = 'https://pypi.org/search/'
    snippets = []
    for page in range(1, 3):
        params = {'q': query, 'page': page}
        r = requests.get(api_url, params=params)
        soup = BeautifulSoup(r.text, 'html5lib')
        snippets += soup.select('a[class*="snippet"]')

    table = Table(title='[not italic]:snake:[/] [bold][magenta]{} [not italic]:snake:[/]'.format(r.url))
    table.add_column('Package', style='bold cyan', no_wrap=True)
    table.add_column('Version', style='bold yellow')
    table.add_column('Released', style='bold green')
    table.add_column('Description', style='bold blue')
    for snippet in snippets:
        link = urljoin(api_url, snippet.get('href'))
        package = snippet.select_one('span[class*="name"]').text.strip()
        version = snippet.select_one('span[class*="version"]').text.strip()
        released = snippet.select_one('span[class*="released"]').text.strip()
        description = snippet.select_one('p[class*="description"]').text.strip()
        table.add_row(package, version, released, description)

    console = Console()
    console.print(table)
    return
