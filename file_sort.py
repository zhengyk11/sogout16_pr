import sys

file_1 = open(sys.argv[1], 'r')
file_2 = open(sys.argv[2], 'r')
output_file = open(sys.argv[3], 'w')

line_1 = file_1.readline().replace('\n', '').split('\t')[1]
line_2 = file_2.readline().replace('\n', '').split('\t')[1]

flag = -1

counter = 0

while 1:
    if cmp(line_1, line_2) < 0:
        counter += 1
        output_file.write(str(counter)+'\t'+line_1+'\n')
        line_1 = file_1.readline()
        if line_1 == '':
            flag = 1
            break
        line_1 = line_1.replace('\n', '').split('\t')[1]
    elif cmp(line_1, line_2) > 0:
        counter += 1
        output_file.write(str(counter)+'\t'+line_2+'\n')
        line_2 = file_2.readline()
        if line_2 == '':
            flag = 2
            break
        line_2 = line_2.replace('\n', '').split('\t')[1]
    else:
        line_1 = file_1.readline()
        if line_1 == '':
            flag = 1
            break
        line_1 = line_1.replace('\n', '').split('\t')[1]

    if counter % 5000 == 0:
        print counter

if flag == 1:
    while 1:
        counter += 1
        output_file.write(str(counter) + '\t' + line_2 + '\n')
        line_2 = file_2.readline()
        if line_2 == '':
            break
        line_2 = line_2.replace('\n', '').split('\t')[1]

        if counter % 5000 == 0:
            print counter

elif flag == 2:
    while 1:
        counter += 1
        output_file.write(str(counter) + '\t' + line_1 + '\n')
        line_1 = file_1.readline()
        if line_1 == '':
            break
        line_1 = line_1.replace('\n', '').split('\t')[1]
        
        if counter % 5000 == 0:
            print counter

print counter
print sys.argv[3]+' done!'

file_1.close()
file_2.close()
output_file.close()