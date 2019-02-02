"""
fout=open("Merged_Input.csv","a")
# first file:

import codecs
with codecs.open("input00", "r",encoding='utf-8', errors='ignore') as fdata:
    for line in fdata:
        fout.write(line)
# now the rest:
for num in range(1,10):
    with codecs.open("input0"+str(num), "r",encoding='utf-8', errors='ignore') as f:
        f.next() # skip the header
        for line in f:
            fout.write(line)

for num in range(10,100):
    with codecs.open("input"+str(num), "r",encoding='utf-8', errors='ignore') as f:
        f.next() # skip the header
        for line in f:
            fout.write(line)

fout.close()
"""
"""
INF 560
"""
# read data and transform to CSV
import gzip

fout=open("Merged_Input.csv","wb")

with gzip.open('input00.gz', 'rb') as fdata:
    fout.write(fdata.read())

for num in range(1,10):
    with gzip.open('input0'+str(num)+'.gz', 'rb') as f:
        f.readline()
        fout.write(f.read())
        print ('%s finined' % num)

for num in range(10,100):
    with gzip.open('input'+str(num)+'.gz', 'rb') as f:
        f.readline()
        fout.write(f.read())
        print ('%s finined' % num)

fout.close()
