# __main__.py
'''
usage: pypi_search.py [-h] query

positional arguments:
  query       terms to search pypi.org package repository

optional arguments:
  -h, --help  show this help message and exit
'''
import sys
import argparse
from pip_search.pip_search import search

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('query', help='terms to search pypi.org package repository') 
    args = ap.parse_args()
    search(args.query)


if __name__ == '__main__':
    sys.exit(main())
