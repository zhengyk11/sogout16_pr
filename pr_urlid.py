from bz2file import BZ2File
import time
import os

M = 1169395307

alpha = 0.15
TN = 30
S = 0.0



outDegree = [0 for i in range(M + 1)]
tmp_value = 1.0/M
pageRank = [tmp_value for i in range(M + 1)]
tmp_value *= alpha
I = [tmp_value for i in range(M + 1)]

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), 'start reading files...'

counter = 0
for fpath, dirs, files in os.walk('/home/luocheng/zhengyukun/link_id'):
    for file in files:
        if file.endswith('.bz2'):
            bz2File = BZ2File(os.path.join(fpath, file), 'r')
            counter += 1
            cnt = 0
            for line in bz2File:
                cnt += 1
                attr = line[:-1].split("<<<")
                id = int(attr[0])
                outDegree[id] = len(attr) - 1
                if cnt % 5000 == 0:
                    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), counter, cnt, file
            bz2File.close()

N = M
# print 'Total number of documents=', N

print '\n#start calculating pagerank...'

for i in range(1, N+1):
    #pageRank[i] = 1.0 / N
    #I[i] = alpha / N
    if outDegree[i] == 0:
        S += pageRank[i]

for k in range(TN):
    counter = 0
    for fpath, dirs, files in os.walk('/home/luocheng/zhengyukun/link_id'):
        for file in files:
            if file.endswith('.bz2'):
                bz2File = BZ2File(os.path.join(fpath, file), 'r')
                counter += 1
                # print os.path.join(fpath, file)
                cnt = 0
                for line in bz2File:
                    cnt += 1
                    attr = line[:-1].split("<<<")
                    id = int(attr[0])
                    for link in attr[1:]:
                        link = int(link)
                        I[link] += (1.0 - alpha) * pageRank[id] / outDegree[id]
                    if cnt % 5000 == 0:
                        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), k, counter, cnt, file
                bz2File.close()

    new_S = 0.0
    for i in range(1, N+1):
        pageRank[i] = I[i] + (1.0 - alpha) * S / N
        I[i] = alpha / N
        if outDegree[i] == 0:
            new_S += pageRank[i]
    print 'iter=', k + 1, ',delta_S=', abs(new_S - S)
    S = new_S

# check whether the sum of pagerank is 1.0
sum = 0.0
for i in range(1, N+1):
    sum += pageRank[i]
print 'Sum of pagerank=', sum

tmp_pr = {}
for i in range(1, N+1):
    tmp_pr[i] = pageRank[i]

pr = sorted(tmp_pr.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

print '\n#write pagerank to file...'

output = open('pr_urlid_1103.txt', 'w')
for i in range(len(pr)):
    output.write(str(i + 1) + '\t' + str(pr[i][0]) + '\t' + str(pr[i][1]) + '\n')
output.close()

print '\n#Top 20 of results:'
for i in range(20):
    print 'rank=', i + 1, ',id=', pr[i][0], ',pr=', pr[i][1]

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print 'Total running time=', str(time.clock()) + 's'

outDegree_file = open('/home/luocheng/zhengyukun/hash2url_result/urlid_outdegree_1103.txt', 'w')

for i in range(1, N+1):
    outDegree_file.write(str(i) + '\t' + str(outDegree[i]) + '\n')

outDegree_file.close()

