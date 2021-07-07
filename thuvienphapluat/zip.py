import gzip
import os
from subprocess import check_call

file_dir = os.getcwd() + "/data/"


def gzipFile(file_path):
    f_in = open(file_path, 'rb')
    f_out = gzip.open(file_path + ".gz", 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()


for i in range(11, 12):
    # gzipFile(file_dir + "part{}".format(i))
    gzipFile(file_dir + "part{}".format(i))
