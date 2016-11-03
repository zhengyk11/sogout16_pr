from bz2file import BZ2File
import time
import os, sys
from urlparse import urlparse
import threading

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sys.argv[1], 'start reading files...'

def readfile(id, tag):
    counter = 0
    for fpath, dirs, files in os.walk('/home/luocheng/zhengyukun/link_data/sogout_data.' + str(id) + '.comp.result'):
        
        if tag == '0':
            files = files[:1024]
        elif tag == '1':
            files = files[1024:2048]
        elif tag == '2':
            files = files[2048:3072]
        elif tag == '3':
            files = files[3072:]
        else:
            return
            
        for file in files:
            if file.endswith('.bz2'):
                file_path = os.path.join(fpath, file)
                output_path = file_path.replace('link_data/', 'link_domain/')
                bz2File = BZ2File(file_path, 'r')
                output = BZ2File(output_path, 'w')

                counter += 1
                #if counter % 200 == 0:
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), counter, file

                for line in bz2File:
                    # convert urls like "http://dalian047120.11467.com/" to "http://dalian047120.11467.com"
                    #line = line.replace('\n', '')
                    # if line.endswith('/'):
                    #     line = line[:-1
                    attr = line[:-1].split("<<<")
                    output.write(attr[0])
                    for a in attr[1:]:
                        try:
                            a_domain = urlparse(a).netloc
                        except ValueError:
                            print "ValueError!"
                            continue
                        
                        output.write('<<<' + a_domain)
                    output.write('\n')
                output.close()
                bz2File.close()

readfile(sys.argv[1], sys.argv[2])

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sys.argv[1], "done!"


# from bz2file import BZ2File
# import time
# import os
# from urlparse import urlparse
# import threading

# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '#start reading files...'

# def readfile(id):
#     counter = 0
#     for fpath, dirs, files in os.walk('/home/luocheng/zhengyukun/link_data/sogout_data.' + str(id) + '.comp.result'):
#         for file in files:
#             if file.endswith('.bz2'):
#                 file_path = os.path.join(fpath, file)
#                 output_path = file_path.replace('link_data/', 'link_domain/')
#                 bz2File = BZ2File(file_path, 'r')
#                 output = BZ2File(output_path, 'w')

#                 counter += 1
#                 #if counter % 200 == 0:
#                 print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), counter, file

#                 for line in bz2File:
#                     # convert urls like "http://dalian047120.11467.com/" to "http://dalian047120.11467.com"
#                     #line = line.replace('\n', '')
#                     # if line.endswith('/'):
#                     #     line = line[:-1
#                     attr = line[:-1].split("<<<")
#                     output.write(attr[0])
#                     for a in attr[1:]:
#                         a_domain = urlparse(a).netloc
#                         output.write('<<<' + a_domain)
#                     output.write('\n')
#                 output.close()
#                 bz2File.close()

# class myThread (threading.Thread):

#     def __init__(self, _id):
#         threading.Thread.__init__(self)
#         self.id = _id


#     def run(self):
#         print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "Starting " + str(self.id)
#         readfile(self.id)


# #threadLock = threading.Lock()
# threads = []

# for i in range(0,10):
#     tmp_thread = myThread(i)
#     threads.append(tmp_thread)
#     tmp_thread.start()

# for t in threads:
#     t.join()

# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "Exiting Main Thread"