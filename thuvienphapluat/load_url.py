import json
import os
from xml.dom.minidom import parse

xml_file = os.path.join(os.getcwd(), "utils", "xml", "{}.xml")
url_file = os.getcwd() + "/utils/url/part{}.txt"


def get_url_from_xml():
    urls = []
    data = []
    for i in range(1, 349):
        doc = parse(xml_file.format(i))
        locs = doc.getElementsByTagName("loc")
        for loc in locs:
            urls.append(loc.firstChild.data)
        if i % 10 == 0:
            data.append(urls)
            urls = []
    data.append(urls)
    return data


def store_data_to_file(data, file):
    with open(file, "a") as f:
        for x in data:
            f.write("{}\n".format(x))


if __name__ == '__main__':
    data = get_url_from_xml()
    for i in range(len(data)):
        store_data_to_file(data[i], url_file.format(i+1))
