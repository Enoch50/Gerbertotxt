import os
import sys
import re
#reading file 
readfilelist=[]
writefilelist=[]
writefilelinenum=[]
mypath=os.path.dirname(sys.argv[0])
os.chdir(mypath)
filelist= os.listdir(mypath)

for files in filelist:
	if files.endswith('gbr'):
		readfilelist.append(files)

readme=file('readme.txt','w')
print >> readme,'Output File:'
for readfile in readfilelist:
	f=file(readfile,'r')
	newfilename=f.name.split('.')[0]+'.txt'
	readme.write(newfilename)
	
	f1=file(newfilename,'w')
	writefilelist.append(newfilename)
	
	lines=f.readlines()
	line_num=0
	line_index=[]
	position=[]
	#finding the pattern
	for line in lines:
		line_num+=1
		has_match=line.find('G01X')
		if has_match==0:
			line_index.append(line_num)
	sides_of_polygon=line_index[1]-line_index[0]-3

	#calculate the position&store them into list
	for line in line_index:
		li=[]
		pattern=re.compile('-?\d{6}')
		for line_offset in range(0,sides_of_polygon-1):		
			s=lines[line+line_offset-1]		
			xpos=pattern.findall(s)[0]
			ypos=pattern.findall(s)[1]
			li.append([float(xpos)/1000,float(ypos)/1000])
		x_average=0
		y_average=0
		for p in li:
			x_average=x_average+p[0]
			y_average=y_average+p[1]
		
		x_average=x_average/len(li)
		y_average=y_average/len(li)
		position.append([x_average,y_average])
	
	position.sort()
	readme.write(' has {:d} lines\n'.format(len(position)))
	#print position
	for pos in position:
		f1.write('X{:07.3f}Y{:07.3f}\n'.format(pos[0],pos[1])) 

	f1.close()
	f.close()
	
readme.close()

