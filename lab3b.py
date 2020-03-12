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
firstNonreservedBlock = 0


def parseCSV(myCSV):
	global freeBlocks, freeInodes, Inodes, numBlocks, numInodes, blockSize, firstNonreservedBlock
	for line in myCSV:
		row = line.split(',') 
		desc = row[0] 

		if desc == "SUPERBLOCK":
			numBlocks = int(row[1])
			numInodes = int(row[2])
			blockSize = int(row[3])
			inodeSize = int(row[4])

		if desc == "GROUP":
			firstInodeNum = int(row[8])

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

	inodeTableSize = (inodeSize * numInodes / blockSize)
	firstNonreservedBlock =  int(firstInodeNum + inodeTableSize)	

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
	global inodes, exitFlag, firstNonreservedBlock, freeBlocks
	myMap = {}
	for inode in inodes:
		inum = inode[1]
		fileSize = int(inode[10])
		fileType=inode[2]
		#print(f"\n{inum}")
		#filetype is 3rd val
		#skip symbolic links with size less than 60; won't have the blocks allocated
		if fileType == 's' and fileSize <= 60:
			continue
		for bnum in range(12,27):
			#print(int(inode[bnum]))
			currBlock=int(inode[bnum])
	
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
				print(f"INVALID {levString}BLOCK {currBlock} IN INODE {inum} AT OFFSET {offset}")
				exitFlag = 1
			elif currBlock < firstNonreservedBlock and currBlock != 0:
				print(f"RESERVED {levString}BLOCK {currBlock} IN INODE {inum} AT OFFSET {offset}")
				exitFlag = 1
			#valid
			else:
				#print(f"\n{currBlock}")	
				if currBlock in myMap:
					myMap[currBlock].append((inum, offset, levString))                                                
				else:
					myMap[currBlock] = [(inum, offset, levString)]

	for indirect in indirects:

		inum = int(indirect[1])
		currBlock = int(indirect[5]) 
		lvlNum = int(indirect[2])
		if lvlNum == 1:
			offset=12
			levString="INDIRECT"

		elif lvlNum == 2:
			offset=268
			levString="DOUBLE INDIRECT"

		elif lvlNum == 3:
			offset=65804
			levString="TRIPLE INDIRECT"

		if currBlock < 0 or currBlock > numBlocks: 
			print(f"INVALID {levString}BLOCK {currBlock} IN INODE {inum} AT OFFSET {offset}")
			exitFlag = 1
		elif currBlock < firstNonreservedBlock and currBlock != 0:
			print(f"RESERVED {levString}BLOCK {currBlock} IN INODE {inum} AT OFFSET {offset}")
			exitFlag = 1
		#valid
		else:
			#print(f"\n{currBlock}")	
			if currBlock in myMap:
				myMap[currBlock].append((inum, offset, levString))                                                
			else:
				myMap[currBlock] = [(inum, offset, levString)]
  
	for block in range(firstNonreservedBlock, numBlocks):
		if block in myMap and block in freeBlocks:
			 print(f"ALLOCATED BLOCK {block} ON FREELIST")
			 exitFlag=1
		elif block not in freeBlocks and block not in myMap:
			print(f"UNREFERENCED BLOCK {block}")
			exitFlag=1
		elif block in myMap and len(myMap[block]) > 1:
			for inum, offset, levString in myMap[block]:
				print(f"DUPLICATE {levString}BLOCK {block} IN INODE {inum} AT OFFSET {offset}")
			exitFlag=1



def checkDirects():
	global exitFlag,directs
	inodeReferences = {}
	parentArr = {}
	for direct in directs:
		dirInode = int(direct[3])
		parentInode = int(direct[1])
		dirInodeName = direct[6]
		if dirInode<0 or dirInode > numInodes:
			print(f"DIRECTORY INODE {parentInode} NAME {dirInodeName} INVALID INODE {dirInode}")
			exitFlag = 1
		if dirInode in freeInodes:
			print(f"DIRECTORY INODE {parentInode} NAME {dirInodeName} UNALLOCATED INODE {dirInode}")
			exitFlag = 1
		if dirInodeName == "'.'" and dirInode != parentInode:
			print(f"DIRECTORY INODE {parentInode} NAME '.' LINK TO INODE {dirInodeName} SHOULD BE {parentInode}")
			exitFlag=1
		if dirInodeName != "'.'" and dirInodeName != "'..'":
			#in parent array, make this inode's parent = the parent in this struct 
			parentArr[dirInode] = parentInode
		inodeReferences[dirInode] = inodeReferences.get(dirInode, 0) +1

	for inode in inodes:
		currInode = int(inode[1])
		#link count is 6th value
		linkCount = int(inode[6])

		if linkCount != inodeReferences.get(currInode, 0):
			print(f"INODE {currInode} HAS {inodeReferences.get(currInode, 0)} LINKS BUT LINKCOUNT IS {linkCount}")
			exitFlag=1

	for direct in directs:
		dirInode = int(direct[3])
		dirInodeName = dirInodeName = direct[6]

		if(dirInodeName) == ".." and dirInode!= parentArr[dirInode]:
			print(f"DIRECTORY INODE {parentInode} NAME '..' LINK TO INODE {dirInode} SHOULD BE {parentArr[dirInode]}")
			exitFlag=1





			
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
	checkDirects()

if(exitFlag):
	exit(2)
else:
	exit(0)

