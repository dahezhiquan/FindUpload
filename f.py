import configparser
import concurrent.futures
from fu import crawl
import datetime

config = configparser.ConfigParser()
config.read('config.ini')
num_threads = config.getint('Settings', 'num_threads')
# 获取当前 scan_count 值
scan_count = config.getint('ScanCount', 'scan_count')

current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# 递增 scan_count 值
scan_count += 1
config.set('ScanCount', 'scan_count', str(scan_count))

# 向结果文件写入当前系统时间
with open("upload.txt", "a") as file:
    file.write("======" + formatted_datetime + "  第" + str(scan_count) + "次扫描" + "======" + "\n")

# 保存更新后的 config.ini 文件
with open('config.ini', 'w') as file:
    config.write(file)

with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(crawl, url) for url in urls]
    concurrent.futures.wait(futures)
