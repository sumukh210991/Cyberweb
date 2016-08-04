#! /usr/bin/env python
"""
	This module creates data file using writetimes data for creating performance 
	plot using gnuplot.
"""
import os, time, math, tempfile, sys
import numpy, datetime, re
from dateutil.relativedelta import relativedelta 
import logging


import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils


#try:
#    import Gnuplot, Gnuplot.PlotItems, Gnuplot.funcutils
#except ImportError:
#    # kludge in case Gnuplot hasn't been installed as a module yet:
#    import __init__
#    Gnuplot = __init__
#    import PlotItems
#    Gnuplot.PlotItems = PlotItems
#    import funcutils
#    Gnuplot.funcutils = funcutils

def main():

	logger = logging.getLogger()
	logger.disabled = False
	l = len(sys.argv)
	min_params = 4

	params = {}		
	parameter_set = ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax', 'plot_file']
	parameter_set_val = {	'xmin' : '', 
							'xmax' : '', 
							'ymin' : '', 
							'ymax' : '', 
							'zmin' : '', 
							'zmax' : '',
							'plot_file' : ''}
	
	feedback = {'error' 	: '',
				'message'	: '',
				'parameters': ''
				}
	
	if l >= min_params :
	   if sys.argv[1] :
		  gridFile = sys.argv[1].strip()
		  parameter_set_val['plot_file'] = gridFile
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Gird Filename file.'
		  print feedback
		  sys.exit()
	   if sys.argv[2] :
		  gridpbsz = sys.argv[2].strip()
	   else :
		  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Grid Problem Size File.'
		  print feedback
		  sys.exit()
	   if sys.argv[3] :
		  plot_filename = sys.argv[3].strip()
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Plot file name.'
		  print feedback
		  sys.exit()
	else:
	   feedback['error'] = 'true'
	   feedback['message'] = ('ERROR:  Not enough args: len = %s' % l)
	   print feedback
	   sys.exit()
	   #print ('ERROR:  Not enough args: len = %s' % l)
	   #sys.exit()
   
   	#check for extra parameters
   	no_extra_params = len(sys.argv) - min_params
   	for i in range(min_params, len(sys.argv)):
		try:
			text = sys.argv[i]
			values = text.split('=')
			if values[0] in parameter_set:
				params[values[0]] = values[1]
			"""else:
				feedback['error'] = 'true'
	   			feedback['message'] = ('Invalid Parameter %s.' % values[0])
	   			print feedback
	   			return
	   		"""
		except Exception as e:
			feedback['error'] = 'true'
	   		feedback['message'] = ('Invalid Parameter Format.')
	   		print feedback
	   		return		
	
	#print params	
	# read grid problem size file
	#file = open(gridpbsz, 'r')
	try:
		file = open(gridpbsz, 'r')
	except Exception as e:
		feedback['error'] = 'true'
	   	feedback['message'] = ('ERROR: %s' % e)
	   	print feedback
	   	return	
	ni = int(float(file.readline().strip()))
	nj = int(float(file.readline().strip()))
	nk = int(float(file.readline().strip()))

	totalCells = ni * nj * nk
	
	# print("ni: %i, nj: %i, nk: %i, total Cells: %i" % (ni, nj, nk, totalCells))
	
	# read grid file
   	#file = open(gridFile, 'r')
	try:
		file = open(gridFile, 'r')
	except Exception as e:
		feedback['error'] = 'true'
	   	feedback['message'] = ('ERROR: %s' % e)
	   	print feedback
	   	return	
	   	
	x = [ [ [ 0.000000 for k in range(nk)] for j in range(nj)] for i in range(ni)]
	y = [ [ [ 0.000000 for k in range(nk)] for j in range(nj)] for i in range(ni)]
	z = [ [ [ 0.000000 for k in range(nk)] for j in range(nj)] for i in range(ni)]	
	
	# reading grid data and storing it values in m3D matrix format
	try:
		for k in range(0, nk):
			for j in range(0, nj):
				for i in range(0, ni):
					line = file.readline().strip()
					if not line:
						break
					values = line.split(',')
					x[i][j][k] = round(float(values[0]), 6)
					y[i][j][k] = round(float(values[1]), 6)
					z[i][j][k] = round(float(values[2]), 6)
	except Exception as e:
		file.close()
		feedback['error'] = 'true'
		feedback['message'] = ('The data file you provided might be in wrong/different format. So, it is giving you following error. ERROR: %s' % e)
		print feedback
		return
	#filename = "bathymetryplotgrid.dat"
	# creating gnuplot compatible data file for ploting bathymetry
	gnuplot_grid_file = gridFile.split('.dat', 1)
	filename = gnuplot_grid_file[0] + '_gnuplot_grid.dat'
	try:
		FILE = open(filename,"w")
	except Exception as e:
		#print "Output File bathymetryplotgrid.dat cant be opened."
	   	feedback['error'] = 'true'
	   	feedback['message'] = ('ERROR: %s' % e)
	   	print feedback
	   	return
		
	#initialize axises min and max values
	x_min = x[0][0][0]
	x_max = x[0][0][0]
	y_min = y[0][0][0]
	y_max = y[0][0][0]
	z_min = z[0][0][0]
	z_max = z[0][0][0]
	
	for i in range(0, ni-1):
		for j in range(0, nj-1):
			zsurf = min(z[i][j])
			if(x_min > x[i][j][0]):
				x_min = x[i][j][0]
			if(x_max < x[i][j][0]):
				x_max = x[i][j][0]
			if(y_min > y[i][j][0]):
				y_min = y[i][j][0]
			if(y_max < y[i][j][0]):
				y_max = y[i][j][0]
			if(z_min > zsurf):
				z_min = zsurf
			if(z_max < zsurf):
				z_max = zsurf
			
			#FILE.write("%i %i %f\n" % (i, j, zsurf))
			FILE.write("%f %f %f\n" % (x[i][j][0], y[i][j][0], zsurf))
		FILE.write("\n")
	
	parameter_set_val["xmin"] = x_min
	parameter_set_val["xmax"] = x_max
	parameter_set_val["ymin"] = y_min
	parameter_set_val["ymax"] = y_max
	parameter_set_val["zmin"] = z_min
	parameter_set_val["zmax"] = z_max
	
	#print "x_min : %f" % x_min
	#print "x_max : %f" % x_max
	#print "y_min : %f" % y_min
	#print "y_max : %f" % y_max
	#print "z_min : %f" % z_min
	#print "z_max : %f" % z_max
	
	"""gnuplot scripts are not completing continuously. to fix it had to add
	#black command to gnuplot after every command
	"""
	
	g = Gnuplot.Gnuplot(debug=0)
	g('    ')
	temp = g.clear()
	g('    ')
	temp = g.title("Bathymetry Plot")
	g('    ')
	
	#add user specific parameters in plot
	for item in params:
		#print item
		parameter_set_val[item] = params[item]	
	
	temp = g('set xrange[%f:%f]' % (float(parameter_set_val['xmin']), float(parameter_set_val["xmax"])))
	g('    ')
	temp = g('set yrange[%f:%f]' % (float(parameter_set_val['ymin']), float(parameter_set_val["ymax"])))
	g('    ')
	temp = g('set zrange[%f:%f]' % (float(parameter_set_val['zmin']), float(parameter_set_val["zmax"])))
	g('    ')
	
	#temp = g('set xtics(0, 20, 40, 60, 80, 100)')
 	#temp = g('set ytics(0, 10, 20, 30, 40)')
 	#temp = g('set ztics(-1, -0.9, -0.8, -0.7, -0.6, -0.5)')
 	temp = g('set xlabel "X"')
 	g('    ')
 	temp = g('set ylabel "Y"')
 	g('    ')
 	temp = g('set zlabel "Z"')
 	g('    ')
 	temp = g('set pm3d at s')
 	g('    ')
 	temp = g('unset contour')
 	g('    ')
 	temp = g('set samples 2')
 	g('    ')
 	temp = g('set key title "Legend"')
 	g('    ')
 	temp = g('set palette defined (0 "#668D3C", 1 "#404F24", 2 "#F5B22A", 3 "#10444C")')
 	#Check this when get some time
 	#temp = g('set palette defined (0 "#986758", 1 "#F8E7B3", 2 "#DBA074", 3 "#2FA3A3")')
	g('    ')
	temp =g('set linetype 1 lw 0.3 lc rgb "black"')
	g('    ')
	temp = g('set view 50, 300')
	g('    ')
	temp = g('unset  key')
	g('    ')
	temp = g.splot(Gnuplot.File(filename, with_='lines'))
	g('    ')
	#temp = g('splot "%s" title "Test Title" with lines' % filename)
	temp = g.hardcopy(plot_filename, terminal='png')
	g('    ')
	
	feedback['error'] = 'false'
	feedback['parameters'] = parameter_set_val
	print feedback
	#print Title
	return "Success"
	
if __name__ == '__main__':
	main()
