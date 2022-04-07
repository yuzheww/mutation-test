"""
This python script computes the Ochiai coverage-based score of .gcov files
for fault localization (locating potential bugs). 

The arguments are a set of .gcov files.
It prints the first 100 most suspicious lines of statements. 
"""



import sys
import math

NUM_FAIL = 0
NUM_PASS = 0
NUM_FILE = len(sys.argv[1:])
SETS = []
# idx = 0
STATUS = []
for arg in sys.argv[1:]:
    if arg[0:4] == 'fail':
        NUM_FAIL = NUM_FAIL + 1
        STATUS.append(False)
    elif arg[0:4] == 'pass':
        NUM_PASS = NUM_PASS + 1
        STATUS.append(True)

    # idx = idx + 1


ALL_SETS = []
TOTAL_LINES = 0

for arg in sys.argv[1:]:
    file1 = open(arg, 'r')
    Lines = file1.readlines()
    mapArr = set()
    for line in Lines:
        tmpArr = line.split(":")
        occur = tmpArr[0].strip()
        lineNum = int(tmpArr[1].strip())
        
        TOTAL_LINES = lineNum

        if (occur.isnumeric()):
            mapArr.add(lineNum)
    ALL_SETS.append(mapArr)


suspiciousness = []
for num in range(TOTAL_LINES):
    
    numfail = 0
    numpass = 0
    # traverse the sets
    for filenum in range(NUM_FILE):
        if (num + 1) in ALL_SETS[filenum]:
            if STATUS[filenum]:
                numpass = numpass + 1
            else:
                numfail = numfail + 1
    sqrt = math.sqrt(NUM_FAIL * (numfail + numpass))
    if sqrt != 0:
        suspiciousness.append((num + 1, numfail / sqrt))
    # else:
    #     suspiciousness[num] = (num + 1, 0.0)

suspiciousness.sort(key = lambda x: x[1], reverse=True)


# print suspicious statements
print(suspiciousness[:100])
