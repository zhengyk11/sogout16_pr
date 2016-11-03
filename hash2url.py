import os
import sys
from bz2 import BZ2File

output_path = sys.argv[1].replace('link_data', 'hash2url_result') + '.txt'


output_file = open(output_path, 'w')

bz2File = BZ2File(sys.argv[1], 'r')
for line in bz2File:
    line = line.replace('/<<<', '<<<').replace('\n', '')
    if line.endswith('/'):
        line = line[:-1]
    attr = line.split('<<<', 2)
    output_file.write(attr[0] + '\t' + attr[1] + '\n')

print sys.argv[1].split('/')[2] + ' done!'
output_file.close()