#!/home/sumukh/env/bin python
"""
	This script checks if the plot image is previously created or not.
	If it is created then it calculates when it was created and is it 
	necessary to create new plot for same job.
"""
import os.path, json, time, math, tempfile, sys, logging, datetime
from dateutil import relativedelta 
from datetime import date
from datetime import datetime

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

	error = ''
	msg = ''
	l = len(sys.argv)
	if l == 2 :
	   if sys.argv[1] :
		  plotFile = sys.argv[1].strip()
	   else :
		  error = 'ERROR: Missing Plot Filename.'
		  return
	else:
	   error = ('ERROR:  Not enough args: len = %s' % l)
	   return
	
	plotNew = ''
	present = ''
	
	# check if file exists
	try:
		exists = os.path.isfile(plotFile)
		if exists:
			present = "true"
		else:
			present = "false"
		#print "Exists"
		#print exists
	except:
		error = 'true'
		msg = "Ooops! Something went wrong while file checking."
	if not exists:
		error = 'false'
		#msg = "File does not exists."
		plotNew = 'true'
	else:
		# print "File exists."
		fileTime = os.path.getmtime(plotFile)
		weekBackDate =  time.mktime((datetime.today() - relativedelta( days = +7 )).timetuple())
		if(weekBackDate > fileTime):
			#print "File was modified before week"
			plotNew = "true"
		else:
			# print "File was modified within a week back"
			plotNew = "false"

	jsonObject = json.dumps({'result': present, 'plotNew' : plotNew, 'error' : error, 'message' : msg})
	print jsonObject
	return
	
if __name__ == '__main__':
	main()
