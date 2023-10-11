import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import configparser
import concurrent.futures

# 读取配置信息
config = configparser.ConfigParser()
config.read('config.ini')

# 读取代理信息和线程数
proxies = {
    'http': config.get('Proxy', 'http'),
    'https': config.get('Proxy', 'https')
}

num_threads = config.getint('Settings', 'num_threads')

# 网站根URL
base_url = 'https://www.splendivilla.com/'  # 替换为你要爬取的网站的根URL

# 已访问的URL列表
visited_urls = []


def crawl(url):
    # 输出当前访问的链接
    print("正在访问链接：", url)

    # 如果已经访问过该URL，则跳过
    if url in visited_urls:
        return

    # 发送GET请求获取网页内容，并使用代理
    response = requests.get(url, proxies=proxies)
    html_content = response.text

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有包含文件上传字段的元素
    input_elements = soup.find_all('input', {'type': 'file'})
    for input_element in input_elements:
        # 打印包含文件上传字段的元素所在链接的信息
        print("在链接 {} 中找到包含文件上传字段的元素".format(url))

    # 将当前URL添加到已访问列表
    visited_urls.append(url)

    # 递归访问页面中的链接
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        absolute_url = urljoin(url, href)

        # 确保链接是以网站根URL开头，并且不在已访问列表中
        if absolute_url.startswith(base_url) and absolute_url not in visited_urls:
            # 使用with语句创建线程池，指定并发线程数
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                # 提交任务到线程池
                future = executor.submit(crawl, absolute_url)
                # 等待任务完成
                future.result()


# 开始爬取网站
crawl(base_url)
