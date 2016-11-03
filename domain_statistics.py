from urlparse import urlparse
import time

print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'starting...'

domain_stats = {}
domain_id = {}

myfile = open('/home/luocheng/zhengyukun/hash2url_result/sorted_all_domain.txt', 'r')

for line in myfile:
    attr = line[:-1].split('\t')

    id = int(attr[0])
    domain = attr[1]

    domain_stats[domain] = 0
    domain_id[domain] = id

myfile.close()

print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'reading sorted_all.txt ...'

counter = 0
myfile = open('/home/luocheng/zhengyukun/hash2url_result/sorted_all.txt', 'r')
for line in myfile:
    attr = line[:-1].split('\t')
    try:
        domain = urlparse(attr[1]).netloc
    except ValueError:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'ValueError:', attr[1]
        continue

    domain_stats[domain] += 1
    counter += 1
    if counter % 500 == 0:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), counter


myfile.close()

output_file = open('/home/luocheng/zhengyukun/hash2url_result/domain_stats.txt', 'w')

domain_list = sorted(domain_stats.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

for d in domain_list:
    output_file.write(str(domain_id[d[0]]) + '\t' + str(d[0]) + '\t' + str(d[1]) + '\n')

output_file.close()
