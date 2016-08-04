#!/usr/bin/python
"""
#! /usr/bin/env python
	This module creates data file using writetimes data for creating performance 
	plot using gnuplot.
"""
import os, time, math, tempfile, sys
import string, json
import numpy, datetime, re
from dateutil.relativedelta import relativedelta 
from dateutil.parser import parser
import logging, subprocess

try:
    import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
except ImportError:
    # kludge in case Gnuplot hasn't been installed as a module yet:
    import __init__
    Gnuplot = __init__
    import PlotItems
    Gnuplot.PlotItems = PlotItems
    import funcutils
    Gnuplot.funcutils = funcutils

def main():

	logger = logging.getLogger()
	logger.disabled = False
	feedback = {	'error' : '',
					'message': '',
					'parameters' : ''
				}

	l = len(sys.argv)
	if l == 5 :
	   if sys.argv[1] :
		  remoteFile = sys.argv[1].strip()
	   else :
		  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Write Times file.'
		  print feedback
		  sys.exit()
	   if sys.argv[2] :
		  plotFile = sys.argv[2].strip()
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing filename for plot.'
		  print feedback
		  sys.exit()
	   if sys.argv[3] :
		  wrtFreq = int(float(sys.argv[3].strip()))
	   else :
	   	  # remove this hard coding when checked by Prof.
	   	  wrtFreq = 10
	   	  #feedback['error'] = 'true'
		  #feedback['message'] = 'ERROR: Missing Write Frequency.'
		  #print feedback
		  #sys.exit()
	   if sys.argv[4] :
		  ID = int(float(sys.argv[4].strip()))
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Write Frequency.'
		  print feedback
		  sys.exit()
	else:
	   feedback['error'] = 'true'
	   feedback['message'] = ('ERROR:  Not enough args: len = %s' % l)
	   print feedback
	   sys.exit()
   
   	# temporary write frequency
   	#wrtFreq = 10.0
	#save time logs in writetimes.dat file
	if(ID != 140112):
		try:
			f = open(remoteFile,'w')
			proc = subprocess.Popen(["ls --full-time OUTPUT/u*.dat"], stdout=subprocess.PIPE, shell=True)
			(writetimes_data, err) = proc.communicate()
			f.write(writetimes_data)
			f.close()
		except Exception as e:
			feedback['error'] = 'true'
		   	feedback['message'] = ('ERROR: %s' % e)
		   	print feedback
		   	return
	try:
		file = open(remoteFile, 'r')
	except Exception as e:
	   feedback['error'] = 'true'
	   feedback['message'] = ('ERROR: %s' % e)
	   print feedback
	   return		
	prevDate = ''
	cumulativeSumCounter = 0
	CumulativeSum = [0.000000000]
	
	try:
		while 1:
			line = file.readline().strip()
			error = 0
			error_msg = ''
			if not line:
				break
			values = line.split(' ')
			currDate = ''
			currTime = ''
			filePresent = 0
			for item in values:
				error = 0
				match = 0
				try:
					datetime.datetime.strptime(item,"%Y-%m-%d")
					currDate = item
					#print currDate
				except ValueError as err:
					error = 1
					# print '%s is not a valid date.' % item
				try:
					datetime.datetime.strptime(item,"%H:%M:%S.000000000")
					currTime = item
					#print currTime
				except ValueError as err:
					error = 1
				if(re.match('^(OUTPUT/)+(u)[0-9]*(.dat)$',item)):
					match = 1
			match = 1
			#print "currDate"
			#print currDate
			#print "currTime"
			#print currTime
			if(currDate != '' and currTime != '' and match == 1):
				try:
					wholeDateTime = currDate + ' ' + currTime
					#print "wholeDateTime"
					#print wholeDateTime
					newDate = datetime.datetime.strptime(wholeDateTime, "%Y-%m-%d %H:%M:%S.000000000")
					#newDate = datetime.datetime.strptime(wholeDateTime, "%Y/%m/%d %H:%M:%S:%f")
				except ValueError as err:
					error = 1
					feedback['error'] = 'true'
					feedback['message'] = 'DateTime conversion error'
					print feedback
					sys.exit()
				if(cumulativeSumCounter == 0):
					newDateSec = time.mktime(newDate.timetuple())
					tstart = time.mktime(newDate.timetuple())
					CumulativeSum[cumulativeSumCounter] = 0
				else:
					newDateSec = time.mktime(newDate.timetuple())
					newSum = newDateSec - prevDate
					CumulativeSum.append(newSum)
				prevDate = newDateSec
				cumulativeSumCounter += 1
	except Exception as e:
		file.close()
		feedback['error'] = 'true'
		feedback['message'] = ('The data file you provided might be in wrong/different format. So, it is giving you following error. ERROR: %s' % e)
		print feedback
		return		
	#print 'Counter: %i' % cumulativeSumCounter
	file.close()
	i=0
	counter = cumulativeSumCounter
	filename = "RunTimePlot.dat"
	try:
		FILE = open(filename,"w")
	except Exception as e:
	   feedback['error'] = 'true'
	   feedback['message'] = ('ERROR: %s' % e)
	   print feedback
	   return		
	FILE.write("#x\ty\n")
	for i in range(0,counter):
		FILE.write("%f" % (wrtFreq * i))
		FILE.write('\t')
		if(i == 0):
			FILE.write("%f" % CumulativeSum[0])
		else:
			FILE.write("%f" % CumulativeSum[i])
		FILE.write('\n')
	FILE.close()
	
	#ploting file
	plotFile = "RunTimePlot.png"
	g = Gnuplot.Gnuplot(debug=0)
	temp = g('clear')	
	temp = g('set title "Run Time Plot"')
	temp = g('set xlabel "Iteration Number"')
	temp = g('set ylabel "Delta T"')
	g('    ')
	g.plot(Gnuplot.File(filename, with_='lines'))
	g('    ')
	#g.plot(Gnuplot.File(filename, every=5, with_='lines'))
	g.hardcopy(plotFile, terminal='png')
	g('    ')
	#temp = g('set terminal png')
	#temp = g('set output "RunTimePlot.png"')
	#temp = g('plot "RunTimePlot.dat" with lines')
	#Title = g('show title')
	del g
	
	feedback['error'] = 'false'
	print feedback
	#print Title
	return
	
if __name__ == '__main__':
    main()