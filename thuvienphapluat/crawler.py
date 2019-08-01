import json
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from helper.multithread_helper import multithread_helper
from bs4 import BeautifulSoup
import gzip
import lxml

url_file = os.getcwd() + "/utils/url/part{}.txt"
data_file = os.getcwd() + "/data/part{}.gz"


def extract_content(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.select("#divThuocTinh > table")[0].find_all('td')
    data = {
        "title": soup.h1.text.strip(),
        "number": tds[1].text.strip(),
        "document_type": tds[4].text.strip(),
        "place_issued": tds[6].text.strip(),
        "signer": tds[9].text.strip(),
        "date_issued": tds[11].text.strip(),
        "content": soup.select("#divContentDoc > div")[0].text.strip(),
    }
    return data


def get_data_from_file(file):
    with open(file, 'r') as f:
        content = f.readlines()
    data = [x.strip() for x in content]
    return data


def store_json_perline_to_file(data, file, is_append=False):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if is_append:
        with gzip.open(file, 'ab') as f:
            for x in data:
                f.write((json.dumps(x, ensure_ascii=False) + '\n').encode('utf-8'))
    else:
        with gzip.open(file, 'wb') as f:
            for x in data:
                f.write((json.dumps(x, ensure_ascii=False) + '\n').encode('utf-8'))


n_success = 0
n_error = 0


def get_data_response(url):
    global n_success, n_error
    resp = requests.get(url)
    if resp.status_code == 200:
        data = extract_content(resp.content)
        n_success += 1
        print("Success: {}, Error: {}".format(n_success, n_error))
        data['url'] = url
        return data
    n_error += 1
    return None


if __name__ == '__main__':
    for i in range(12, 36):
        urls = get_data_from_file(url_file.format(i))
        for j in range(10):
            data = multithread_helper(urls[j*10:(j+1)*10], get_data_response, timeout_concurrent_by_second=720, max_workers=50,
                                  debug=False)
            store_json_perline_to_file(data, data_file.format(i), True)
