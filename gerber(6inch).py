# coding:utf-8
import os
import sys
import re
#reading file 
readfilelist=[]
writefilelist=[]
mypath=os.path.dirname(sys.argv[0])
mypath=os.path.abspath(mypath)
os.chdir(mypath)
filelist= os.listdir(mypath)

for files in filelist:
	if os.path.splitext(files)[1]=='.gbr':
		readfilelist.append(files)
readme=file('readme.txt','w')
print >> readme,'Output File:'

for readfile in readfilelist:
	filetoread=file(readfile,'r')
	newfilename=filetoread.name.split('.')[0]+'.txt'
	readme.write(newfilename)
	filetowrite=file(newfilename,'w')
	writefilelist.append(newfilename)
	dataset=[]
	x_average=0
	y_average=0
	counter=0	
	flag=0

	for line in filetoread.readlines():
		pattern1=re.compile('-?\d{6}')
		pattern2=re.compile('G01X')
		pattern3=re.compile('D02|M02')
		pos=pattern1.findall(line)
		newblockflag=pattern2.search(line)
		endblockflag=pattern3.search(line)
		if newblockflag:
			flag=1
		if flag==1 and len(pos)==2 and endblockflag==None:
			counter += 1
			x_average += float(pos[0])/1000
			y_average += float(pos[1])/1000
		if flag==1 and endblockflag:
			x_average=x_average/counter
			y_average=y_average/counter
			dataset.append([x_average,y_average])	
			x_average=0
			y_average=0
			counter=0	
			flag=0     
	dataset.sort()
	readme.write(' has {:d} lines\n'.format(len(dataset)))
	for pos in dataset:
		filetowrite.write('X{:07.3f}Y{:07.3f}\n'.format(pos[0],pos[1])) 
	filetoread.close()
	filetowrite.close()	
readme.close()	
