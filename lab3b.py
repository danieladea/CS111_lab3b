import sys, string, locale, csv


freeBlocks = [] 
freeInodes = []
inodes = []
indirects = []
directs = []

numBlocks = 0
numInodes = 0
exitFlag = 0
blockSize = 0
reservedBlocks = {0,1,2,3,4,5,6,7}
inodeLinks = {}
usedBlocks = {} 



def parseCSV(myCSV):
	global freeBlocks, freeInodes, Inodes, numBlocks, numInodes, blockSize
	for line in myCSV:
		row = line.split(',') 
		desc = row[0] 

		if desc == "SUPERBLOCK":
			numBlocks = int(row[1])
			numInodes = int(row[2])
			blockSize = int(row[3])

		elif desc == "BFREE":
			freeBlocks.append(int(row[1]))

		elif desc == "IFREE":
			freeInodes.append(int(row[1]))

		elif desc == "INODE":
			inodes.append(row)
		
		elif desc == "INDIRECT":
			indirects.append(row)
		
		elif desc == "DIRENT":
			directs.append(row)

def checkInodes():
	global freeInodes, inodes, exitFlag
	for inode in inodes:

		num = inode[1] 
		fileType = inode[2]

		if fileType != "0" and num in freeInodes:
			exitFlag = 1
			print(f"ALLOCATED INODE {num} ON FREELIST")
		elif fileType==0 and num not in freeNodes:
			exitFlag = 1
			printf(f"UNALLOCATED INODE {num} NOT ON FREELIST")
		
def checkBlocks():
	global inodes, exitFlag
	for inode in inodes:
		inum = inode[1]
		print(f"\n{inum}")
		for bnum in range(12,27):
			print(int(inode[bnum]))
			currBlock=int(inode[bnum])
			
			if currBlock < 0 or currBlock> numBlocks:
				if bnum == 24:
					offset=12
					lev=1
					levString="INDIRECT "
				elif bnum == 25:
					offset=268
					lev=2
					levString="DOUBLE INDIRECT "
				elif bnum == 26:
					offset=65804
					lev=3
					levString="TRIPLE INDIRECT "
				else:
					offset=0
					lev=0
					levString=""
				if currBlock < 0 or currBlock > numBlocks: 
					print(f"INVALID {levString}BLOCK {str(currBlock)} IN INODE {str(inum)} AT OFFSET {str(offset)}\n")
					exitFlag = 1
				elif currBlock in reservedBlocks and currBlock != 0:
					print(f"RESERVED {levString}BLOCK {str(currBlock)} IN INODE {str(inum)} AT OFFSET {str(offset)}\n")
					exitFlag = 1
			
if __name__ == '__main__':

	if len(sys.argv) != 2:
		sys.stderr.write('Only one filename allowed for running.\n')
		exit(1)
	#Following is for taking in the file and begin processing it!
	try:
		readCSV = open(sys.argv[1] , "r");
	except:
		sys.stderr.write("Could not find file.\n")
		exit(1)

	parseCSV(readCSV)
	checkInodes()
	checkBlocks()
	#checkDirects()

if(exitFlag):
	exit(2)
else:
	exit(0)
