from bz2file import BZ2File
import time
import os

alpha = 0.15
TN = 30
S = 0.0

outDegree = {}
pageRank = {}
I = {}

#output_file = open('/home/luocheng/zhengyukun/myoutput/pr_domain.log', 'w')

path = '/home/luocheng/zhengyukun/link_domain'

domain_file = open('/home/luocheng/zhengyukun/hash2url_result/sorted_all_domain.txt', 'r')

cnt = 0

for line in domain_file:
    attr = line[:-1].split('\t')
    outDegree[attr[1]] = 0
    cnt += 1
    if cnt % 50000 == 0:
        print cnt

print '###'+str(len(outDegree))

domain_file.close()

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'start reading files...'

counter = 0
for fpath, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.bz2'):
            bz2File = BZ2File(os.path.join(fpath, file), 'r')
            counter += 1
            cnt = 0
            for line in bz2File:
                cnt += 1
                if cnt % 5000 == 0:
                    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), counter, cnt, file
                attr = line[:-1].split("<<<")
                #outDegree[attr[1]] = 0
                for a in attr[2:]:
                    if a in outDegree:
                        outDegree[attr[1]] += 1
            #print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), counter, file
            bz2File.close()

N = len(outDegree)
#print 'Total number of documents=', N

print 'start calculating pagerank...'

for i in outDegree:
    pageRank[i] = 1.0 / N
    I[i] = alpha / N
    if outDegree[i] == 0:
        S += pageRank[i]

for k in range(TN):
    counter = 0
    for fpath, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.bz2'):
                bz2File = BZ2File(os.path.join(fpath, file), 'r')
                counter += 1
                cnt = 0
                #print os.path.join(fpath, file)
                for line in bz2File:
                    attr = line[:-1].split("<<<")
                    cnt+= 1
                    if cnt % 10000 == 0:
                        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), k, counter, cnt, file
                    i = attr[1]
                    for j in attr[2:]:
                        if j not in outDegree:
                            continue
                        I[j] += (1.0 - alpha) * pageRank[i] / outDegree[i]
                bz2File.close()

    new_S = 0.0
    for i in outDegree:
        pageRank[i] = I[i] + (1.0 - alpha) * S / N
        I[i] = alpha / N
        if outDegree[i] == 0:
            new_S += pageRank[i]
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'iter=', (k+1), ',delta_S=', abs(new_S - S)
    # if abs(new_S - S) < 1e-15:
    #     break
    S = new_S

# check whether the sum of pagerank is 1.0
sum = 0.0
for i in pageRank:
    sum += pageRank[i]
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'Sum of pagerank=', sum

pr = sorted(pageRank.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'write pagerank to file...'

output = open('/home/luocheng/zhengyukun/hash2url_result/pr_domain_1103.txt', 'w')
for i in range(len(pr)):
    output.write(str(i+1)+'\t'+str(pr[i][1])+'\t'+str(pr[i][0])+'\n')
output.close()

# print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), '#Top 20 of results:'
# for i in range(20):
#     print 'rank=', i+1, ',pr=', pr[i][1], ',url=', pr[i][0]

print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'Total running time=', time.clock(), 's'

outDegree_file = open('/home/luocheng/zhengyukun/hash2url_result/domain_outdegree_1103.txt', 'w')

for i in outDegree:
    outDegree_file.write(str(i) + '\t' + str(outDegree[i]) +'\n')

outDegree_file.close()
