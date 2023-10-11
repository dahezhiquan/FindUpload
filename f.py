import configparser
import concurrent.futures
from fu import crawl

config = configparser.ConfigParser()
config.read('config.ini')
num_threads = config.getint('Settings', 'num_threads')

with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(crawl, url) for url in urls]
    concurrent.futures.wait(futures)
