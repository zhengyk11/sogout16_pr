#import sys
import os
import time
import threading
from bz2file import BZ2File

print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'starting...'

all_name = '/home/luocheng/zhengyukun/hash2url_result/sorted_all.txt'
#data_name = sys.argv[2]

all = open(all_name, 'r')

url_dict = {}
counter = 0
for line in all:
    counter += 1
    if counter % 5000 == 0:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), counter
    attr = line[:-1].split('\t')
    id = int(attr[0])
    url = attr[1]
    url_dict[url] = id

print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '###counter=', counter
all.close()


def url2id(data_name, tag):
    counter = 0
    str_1 = '/home/luocheng/zhengyukun/link_data/sogout_data.'
    str_2 = '.comp.result'
    data_name = str_1 + str(data_name) + str_2
    for fpath, dirs, files in os.walk(data_name):
        if tag == 0:
            files = files[0:1024]
        elif tag == 1:
            files = files[1024:2048]
        elif tag == 2:
            files = files[2048:3072]
        else:
            files = files[3072:]

        for file in files:
            if file.endswith('.bz2'):
                file_path = os.path.join(fpath, file)
                output_path = file_path.replace('link_data/', 'link_id/')
                if os.path.exists(output_path):
                    continue
                counter += 1
                print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), counter, file
                f = BZ2File(file_path, 'r')
                output = BZ2File(output_path, 'w')
                for line in f:
                    line = line[:-1].replace('/<<<', '<<<')
                    # line = line.replace('<<<http://http://', '<<<http://')
                    if line.endswith('/'):
                        line = line[:-1]
                    attr = line.split('<<<')
                    if attr[1] not in url_dict:
                        print 'error!', file, attr[1]
                        continue
                    new_line = str(url_dict[attr[1]])
                    for a in attr[2:]:
                        a = str(a)
                        if a.startswith('http://http://'):
                            a = a[7:]
                        if a in url_dict:
                            new_line += '<<<' + str(url_dict[a])
                    output.write(new_line + '\n')
                f.close()
                output.close()
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'Thread ' + data_name + ' ' + str(tag) + ' done!'

# try:
#     for i in range(1,10):
#         for tag in range(4):
#             thread.start_new_thread(url2id, (i,tag,))
#     #thread.start_new_thread(url2id, ("Thread-2", 4,))
# except:
#     print "Error: unable to start thread"


class myThread (threading.Thread):

    def __init__(self, _i, _tag):
        threading.Thread.__init__(self)
        self.i = _i
        self.tag = _tag

    def run(self):
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Starting " + str(self.i) + ' ' + str(self.tag)
        #threadLock.acquire()
        url2id(self.i, self.tag)
        #threadLock.release()

#threadLock = threading.Lock()
threads = []

for i in range(1,10):
    for tag in range(4):
        tmp_thread = myThread(i, tag)
        threads.append(tmp_thread)
        tmp_thread.start()
        #thread.start_new_thread(url2id, (i,tag,))

for t in threads:
    t.join()

print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Exiting Main Thread"
