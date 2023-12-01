import configparser
import concurrent.futures
from fu import crawl
from category.find_login import login
import datetime
import argparse

# 外部args参数处理

parser = argparse.ArgumentParser(description='梦想是做你的贴身渗透测试伴侣')

# 添加命令行参数
parser.add_argument('-l', action='store_true', help='扫描登录框')
parser.add_argument('-u', action='store_true', help='扫描上传点')
args = parser.parse_args()

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

with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

# 扫描上传点
if args.u:
    # 向结果文件写入当前系统时间
    with open("upload.txt", "a") as file:
        file.write("======" + formatted_datetime + "  第" + str(scan_count) + "次扫描" + "======" + "\n")
    # 保存更新后的 config.ini 文件
    with open('config.ini', 'w') as file:
        config.write(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(crawl, url) for url in urls]
        concurrent.futures.wait(futures)

# 扫描登录点
if args.l:
    # 向结果文件写入当前系统时间
    with open("login.txt", "a") as file:
        file.write("======" + formatted_datetime + "  第" + str(scan_count) + "次扫描" + "======" + "\n")
    # 保存更新后的 config.ini 文件
    with open('config.ini', 'w') as file:
        config.write(file)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(login, url) for url in urls]
        concurrent.futures.wait(futures)
