#! /usr/bin/env python
#####
import sys
import os, time, math, tempfile
import numpy
from subprocess import Popen,PIPE

def main():
	l = len(sys.argv)
	if l == 3 :
		if sys.argv[1] :
			cwhost = sys.argv[1].strip()
		else :
			print 'ERROR: Missing HostName.'
			sys.exit()
		if sys.argv[2] :
			file = sys.argv[2].strip()
		else :
			print 'ERROR: Missing FileName.'
			sys.exit()
	
	else:
	   print ('ERROR:  Not enough args: len = %s' % l)
	   sys.exit()
   
	# file = open(remoteFile, 'r')
	f = open(file, 'r')
	str = f.readline().strip()
	str = str.replace('[', '')
	str = str.replace(']', '')
	str = str.strip()
	str = str.split(',', 1)
	str2 = str[1].split(' ', 1)
	#print str2[0]
	
	str = f.readline().strip()
	str = str.replace('[', '')
	str = str.replace(']', '')
	str = str.strip()
	str = str.split(',', 1)
	str2 = str[1].split(' ', 1)
	#print str2[0]
	
	str = f.readline().strip()
	str = str.replace('[', '')
	str = str.replace(']', '')
	str = str.strip()
	str = str.split(',', 1)
	str2 = str[1].split(' ', 1)
	#print str2[0]
	
	str = f.readline().strip()
	str = str.replace('[', '')
	str = str.replace(']', '')
	str = str.strip()
	str = str.split(',', 1)
	str2 = str[1].split(' ', 1)
	#print str2[0]
	
	CumulativeSum = [0]
	CumulativeSumEveryNth = [0]
	x = 0
	if str2[0] == 'TPres':
		str3 = str2[1].split('}  {')
		for i in range(len(str3)):
			str3[i] = str3[i].replace('{', '')
			str3[i] = str3[i].replace('}', '')
			data = str3[i].split(',')
			#print i 
			#print '\t'
			initial = eval(data[1].strip())
			#print initial 
			#print '\t'
			end = eval(data[2].strip())
			#print end 
			#print '\t'
			if(len(CumulativeSum) == 1 and x == 0): 
				CumulativeSum[0] = math.fabs(end - initial)
				CumulativeSumEveryNth[0] = math.fabs(end - initial)
				x = 1
			else:
				if(i%200 == 0):
					CumulativeSumEveryNth.append(math.fabs(end - initial + CumulativeSum[i-1]))
				CumulativeSum.append(math.fabs(end - initial + CumulativeSum[i-1]))
			#print CumulativeSum[i]
			#print '\n'
	
	
	str = f.readline().strip()
	str = str.replace('[', '')
	str = str.replace(']', '')
	str = str.strip()
	str = str.split(',', 1)
	str2 = str[1].split(' ', 1)
	#print str2[0]
	
	CumulativeSumVel = [0]
	CumulativeSumVelEveryNth = [0]
	x = 0
	if str2[0] == 'TVel':
		str4 = str2[1].split('}  {')
		for i in range(len(str4)):
			str4[i] = str4[i].replace('{', '')
			str4[i] = str4[i].replace('}', '')
			data = str4[i].split(',')
			#print i 
			#print '\t'
			initial = eval(data[1].strip())
			#print initial 
			#print '\t'
			end = eval(data[2].strip())
			#print end 
			#print '\t'
			if(len(CumulativeSumVel) == 1 and x == 0): 
				CumulativeSumVel[0] = math.fabs(end - initial)
				CumulativeSumVelEveryNth[0] = math.fabs(end - initial)
				x = 1
			else: 
				if(i%400 == 0):
					CumulativeSumVelEveryNth.append(math.fabs(end - initial + CumulativeSumVel[i-1]))
				CumulativeSumVel.append(math.fabs(end - initial + CumulativeSumVel[i-1]))

	str = f.readline().strip()
	str = str.replace('[', '')
	str = str.replace(']', '')
	str = str.strip()
	str = str.split(',', 1)
	str2 = str[1].split(' ', 1)

	CumulativeSumFile = [0]
	x = 0
	if str2[0] == 'Tfile':
		str4 = str2[1].split('}  {')
		for i in range(len(str4)):
			str4[i] = str4[i].replace('{', '')
			str4[i] = str4[i].replace('}', '')
			data = str4[i].split(',')
			initial = eval(data[1].strip())
			end = eval(data[2].strip())
			if(len(CumulativeSumFile) == 1 and x == 0): 
				CumulativeSumFile[0] = math.fabs(end - initial)
				x = 1
			else: 
				CumulativeSumFile.append(math.fabs(end - initial + CumulativeSumFile[i-1]))

			
	#print 'Elements in CumulativeSum: %d' % len(CumulativeSum)
	f.close()
	
	filename = "parsing.dat"
	try:
		FILE = open(filename,"w")
	except:
		print "File parsing.dat cant be opened."
		sys.exit()
	for i in range(len(CumulativeSum)):
		FILE.write("%i" % i )
		FILE.write('\t')
		FILE.write("%f" % CumulativeSum[i])
		FILE.write('\n')
	
	FILE.close()


	filenamePressEveryNth = "parsingPressEveryNth.dat"
	try:
		FILE = open(filenamePressEveryNth,"w")
	except:
		print "File parsing.dat cant be opened."
		sys.exit()
	for i in range(len(CumulativeSumEveryNth)):
		y = i*200
		FILE.write("%i" % y)
		FILE.write('\t')
		FILE.write("%f" % CumulativeSumEveryNth[i])
		FILE.write('\n')
	
	FILE.close()

	filename1 = "parsingVel.dat"
	try:
		FILE = open(filename1,"w")
	except:
		print "File parsing.dat cant be opened."
		sys.exit()
	for i in range(len(CumulativeSumVel)):
		FILE.write("%i" % i )
		FILE.write('\t')
		FILE.write("%f" % CumulativeSumVel[i])
		FILE.write('\n')
	
	FILE.close()

	filenameVelocityEveryNth = "filenameVelocityEveryNth.dat"
	try:
		FILE = open(filenameVelocityEveryNth,"w")
	except:
		print "File parsing.dat cant be opened."
		sys.exit()
	for i in range(len(CumulativeSumVelEveryNth)):
		y = i*400
		FILE.write("%i" %  y)
		FILE.write('\t')
		FILE.write("%f" % CumulativeSumVelEveryNth[i])
		FILE.write('\n')
	
	FILE.close()

	filename2 = "parsingFile.dat"
	try:
		FILE = open(filename2,"w")
	except:
		print "File parsing.dat cant be opened."
		sys.exit()
	for i in range(len(CumulativeSumFile)):
		FILE.write("%i" % i )
		FILE.write('\t')
		FILE.write("%f" % CumulativeSumFile[i])
		FILE.write('\n')
	
	FILE.close()
	return 'Success'

	# ploting file
	# 	g = Gnuplot.Gnuplot(debug=1)
	# 	g.clear()
	# 	g.title('Pressure Timing plot')
	# 	g.xlabel('MaxFileNo * Writeout freq.(Iterations)')
	# 	g.ylabel('Y-Axis: Cumulative Sum')
	# 	g.plot(Gnuplot.File(filename, with_='lines'))
	# 	#g.plot(Gnuplot.File(filename, every=5, with_='lines'))
	# 	g.hardcopy('parsing.svg', terminal='svg')
	# 	#wait()
	# 	g.plot(Gnuplot.File(filename, with_='lines'))
	# 	g.hardcopy('parsing.ps', mode='eps')
	# 
	# 	g.clear()
	# 	g.title('Velocity Timing plot')
	# 	g.xlabel('MaxFileNo * Writeout freq.(Iterations)')
	# 	g.ylabel('Y-Axis: Cumulative Sum')
	# 	g.plot(Gnuplot.File(filename1, with_='lines'))
	# 	#g.plot(Gnuplot.File(filename, every=5, with_='lines'))
	# 	g.hardcopy('parsingVel.svg', terminal='svg')
	# 	#wait()
	# 	g.plot(Gnuplot.File(filename1, with_='lines'))
	# 	g.hardcopy('parsingVel.ps', mode='eps')
	# 
	# 	g.clear()
	# 	g.title('Vel_Cor Timing plot')
	# 	g.xlabel('MaxFileNo * Writeout freq.(Iterations)')
	# 	g.ylabel('Y-Axis: Cumulative Sum')
	# 	g.plot(Gnuplot.File(filename2, with_='lines'))
	# 	#g.plot(Gnuplot.File(filename, every=5, with_='lines'))
	# 	g.hardcopy('parsingVel_Cor.svg', terminal='svg')
	# 	#wait()
	# 	g.plot(Gnuplot.File(filename1, with_='lines'))
	# 	g.hardcopy('parsingVel_Cor.ps', mode='eps')


if __name__ == '__main__':
    main()