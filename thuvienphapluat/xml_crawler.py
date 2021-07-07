import os
import requests
import time

url = "https://thuvienphapluat.vn/sitemap{}.xml"
file_dir = os.path.join(os.getcwd(), "utils", "xml")
file = os.path.join(file_dir, "{}.xml")
print(file)


def load_xml(url, file):
    response = requests.get(url)
    with open(file, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    tic = time.time()
    error = 0
    for i in range(1, 349):
        print("Sitemap {}:".format(i), url.format(i), end=" ")
        try:
            load_xml(url.format(i), file.format(i))
            print("Success")
        except Exception as e:
            error += 1
            print(e)
            #print("Error")

    toc = time.time()
    print("Time processing: ", toc - tic, "s")
    print("Error: ", error)
