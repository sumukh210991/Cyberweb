#! /usr/bin/env python
"""
	This script creates contour movie using job output files u, v, w and bathymetry grid.
"""
import os, time, math, tempfile, sys
import numpy, datetime, re
from dateutil.relativedelta import relativedelta 
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

feedback = {'error' 	: '',
			'message'	: '',
			'parameters': ''
			}

outputfile_list = []

def main():
	
	logger = logging.getLogger()
	logger.disabled = False
	l = len(sys.argv)
	min_params = 14
	
	params = {}		
	parameter_set = ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax', 'plot_file']
	parameter_set_val = {	'plot_type' : '',
							'output_format' : '',
							'view_plane' : '',
							'input_parameter' : '',
							'kMax' : '',
							'jMax' : '',
							'iMax' : '',
							'grid_file' : '', 
							'Version' : '', 
							'Skip' : '', 
							'ETime' : '', 
							'STime' : '', 
							'job_name' : '',
							'home_dir' : ''}
	
	
	if l >= min_params :
	   if sys.argv[1] :
		  home_dir = sys.argv[1].strip()
		  parameter_set_val['home_dir'] = home_dir
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Home directory path.'
		  print feedback
		  sys.exit()
	   if sys.argv[2] :
		  job_name = sys.argv[2].strip()
		  parameter_set_val['job_name'] = job_name
	   else :
		  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Job name.'
		  print feedback
		  sys.exit()
	   if sys.argv[3] :
		  STime = sys.argv[3].strip()
		  parameter_set_val['STime'] = STime
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Start Time.'
		  print feedback
		  sys.exit()
	   if sys.argv[4] :
		  ETime = sys.argv[4].strip()
		  parameter_set_val['ETime'] = ETime
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing End Time.'
		  print feedback
		  sys.exit()
	   if sys.argv[5] :
		  Skip = sys.argv[5].strip()
		  parameter_set_val['Skip'] = Skip
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Skip Time.'
		  print feedback
		  sys.exit()
	   if sys.argv[6] :
		  Version = sys.argv[6].strip()
		  parameter_set_val['Version'] = Version
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Version.'
		  print feedback
		  sys.exit()
	   if sys.argv[7] :
		  grid_file = sys.argv[7].strip()
		  parameter_set_val['grid_file'] = grid_file
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Grid File name.'
		  print feedback
		  sys.exit()
	   if sys.argv[8] :
		  iMax = int(sys.argv[8].strip())
		  parameter_set_val['iMax'] = iMax
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing iMax value.'
		  print feedback
		  sys.exit()
	   if sys.argv[9] :
		  jMax = int(sys.argv[9].strip())
		  parameter_set_val['jMax'] = jMax
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing jMax value.'
		  print feedback
		  sys.exit()
	   if sys.argv[10] :
		  kMax = int(sys.argv[10].strip())
		  parameter_set_val['kMax'] = kMax
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing kMax value.'
		  print feedback
		  sys.exit()
	   if sys.argv[11] :
		  input_parameter = sys.argv[11].strip()
		  parameter_set_val['input_parameter'] = input_parameter
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Input parameter.'
		  print feedback
		  sys.exit()
	   if sys.argv[12] :
		  view_plane = sys.argv[12].strip()
		  parameter_set_val['view_plane'] = view_plane
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing View Plane.'
		  print feedback
		  sys.exit()
	   if sys.argv[13] :
		  output_format = sys.argv[13].strip()
		  parameter_set_val['output_format'] = output_format
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Output Format.'
		  print feedback
		  sys.exit()
	   if sys.argv[14] :
		  plot_type = sys.argv[14].strip()
		  parameter_set_val['plot_type'] = plot_type
	   else :
	   	  feedback['error'] = 'true'
		  feedback['message'] = 'ERROR: Missing Output Format.'
		  print feedback
		  sys.exit()

	else:
	   feedback['error'] = 'true'
	   feedback['message'] = ('ERROR:  Not enough args: len = %s' % l)
	   print feedback
	   sys.exit()

	#default number of contours 
	NContour=20
	J=16
	fps=5      # Frame per seconds.
	NRepeat=1   # How many times to repeat the movie.
	input_dir = ('%s/%s/OUTPUT' % (home_dir, job_name))
	#print input_dir
	max_file = 0
	try:
		proc = subprocess.Popen(["ls -al u*.dat | wc"], stdout=subprocess.PIPE, shell=True)
		(output, err) = proc.communicate()
		values = output.split()
		max_file = int(int(values[0]) - 1)
		
	except Exception as e:
		feedback['error'] = 'true'
	   	feedback['message'] = ('ERROR: %s' % e)
	   	print feedback
	   	return
	
	ETime = max_file
	
	Frames=MakeContourVerticalMovie_ascii(job_name, input_dir,grid_file,Version,STime,Skip,ETime,iMax,jMax,kMax,J,NContour, input_parameter, view_plane, output_format, plot_type);
	if(output_format == 'contour_movie'):
		movie = CreateMovie(job_name, input_parameter, view_plane, plot_type)
		#movie = job_name + '_' + input_parameter+ '_' + view_plane + "_contourmovie.mp4"
		feedback['output_name'] = movie
	elif(output_format == 'contour_image'):
		feedback['output_name'] = Frames
	elif(output_format == 'contour_sequence'):
		feedback['output_name'] = outputfile_list
	feedback['error'] = 'false'
	#movie = CreateMovie(job_name, input_parameter, view_plane)
	#print "Success"		
	print feedback
	DeleteUnwantedFiles()
	return #"Success"

def DeleteUnwantedFiles():
	
	
	return
	
def MakeContourVerticalMovie_ascii(job_name, input_dir,grid_file,Version,STime,Skip,ETime,iMax,jMax,kMax,J,NContour, input_parameter, view_plane, output_format, plot_type):
	
	#Initializing
	FrameCounter=1;
	
	# read grid file
   	try:
		file = open(grid_file, 'r')
	except Exception as e:
		feedback['error'] = 'true'
	   	feedback['message'] = ('ERROR: %s' % e)
	   	print feedback
	   	return	
	   	
	x = [ [ [ 0.000000 for k in range(kMax)] for j in range(jMax)] for i in range(iMax)]
	y = [ [ [ 0.000000 for k in range(kMax)] for j in range(jMax)] for i in range(iMax)]
	z = [ [ [ 0.000000 for k in range(kMax)] for j in range(jMax)] for i in range(iMax)]	
	
	# reading grid data and storing it values in 3D matrix format
	try:
		for k in range(0, kMax):
			for j in range(0, jMax):
				for i in range(0, iMax):
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
	
	(Xc, Yc, Zc) = CalCenter(x ,y ,z, iMax,jMax,kMax);

	if(view_plane == 'XZ' or view_plane == 'ZX'):
		J = int(jMax/2)
		X = Xc[:,J,:].reshape(iMax-1, kMax-1)
		Y = Zc[:,J,:].reshape(iMax-1, kMax-1)
	elif(view_plane == 'XY' or view_plane == 'YX'):
		J = int(kMax/2)
		X = Xc[:,:,J].reshape(iMax-1, jMax-1)
		Y = Yc[:,:,J].reshape(iMax-1, jMax-1)
	elif(view_plane == 'YZ' or view_plane == 'ZY'):
		J = int(iMax/2)
		X = Yc[J,:,:].reshape(jMax-1, kMax-1)
		Y = Zc[J,:,:].reshape(jMax-1, kMax-1)
	#print J
	MinX=X.min();
	MaxX=X.max();
	MinY=Y.min();
	MaxY=Y.max();	
	
	if(output_format == 'contour_movie' or output_format == 'contour_sequence'):
		i = int(float(STime))
		counter = 0
		skip_time = int((int(float(ETime)) - int(float(STime)))/10)
		#for I in xrange(int(float(STime)), int(float(ETime)), int(float(Skip))):
		for I in xrange(int(float(STime)), int(float(ETime)), skip_time):
			#plottinDataManipulation(job_name, input_dir,grid_file,Version,STime,Skip,ETime,iMax,jMax,kMax,J,NContour, input_parameter, view_plane, output_format, I)	
			if(input_parameter == 'velocity'):
				u=ReadField('u',I,input_dir,Version,iMax,jMax,kMax)
				v=ReadField('v',I,input_dir,Version,iMax,jMax,kMax)
				w=ReadField('w',I,input_dir,Version,iMax,jMax,kMax)
				################################
				[uc, vc, wc] = VecToCenter(u,v,w,iMax,jMax,kMax)
				################################
				if(view_plane == 'XZ' or view_plane == 'ZX'):
					Data = (((uc[:,J,:]**2) + (vc[:,J,:]**2) + (wc[:,J,:]**2))**0.5).reshape(iMax-1, kMax-1)
					U = uc[:,J,:].reshape(iMax-1, kMax-1)
					V = vc[:,J,:].reshape(iMax-1, kMax-1)
					W = wc[:,J,:].reshape(iMax-1, kMax-1)
				elif(view_plane == 'XY' or view_plane == 'YX'):
					Data = (((uc[:,:,J]**2) + (vc[:,:,J]**2) + (wc[:,:,J]**2))**0.5).reshape(iMax-1, jMax-1)
					U = uc[:,:,J].reshape(iMax-1, jMax-1)
					V = vc[:,:,J].reshape(iMax-1, jMax-1)
					W = wc[:,:,J].reshape(iMax-1, jMax-1)
				elif(view_plane == 'YZ' or view_plane == 'ZY'):
					Data = (((uc[J,:,:]**2) + (vc[J,:,:]**2) + (wc[J,:,:]**2))**0.5).reshape(jMax-1, kMax-1)
					U = uc[J,:,:].reshape(jMax-1, kMax-1)
					V = vc[J,:,:].reshape(jMax-1, kMax-1)
					W = wc[J,:,:].reshape(jMax-1, kMax-1)
					
			elif(input_parameter == 'pressure'):
				p = ReadField('p',I,input_dir,Version,iMax,jMax,kMax)
				p = p.astype(numpy.float)
				if(view_plane == 'XZ' or view_plane == 'ZX'):
					Data = ((p[:,J,:]**2)**0.5).reshape(iMax-1, kMax-1)
				elif(view_plane == 'XY' or view_plane == 'YX'):
					Data = ((p[:,:,J]**2)**0.5).reshape(iMax-1, jMax-1)
				elif(view_plane == 'YZ' or view_plane == 'ZY'):
					Data = ((p[J,:,:]**2)**0.5).reshape(jMax-1, kMax-1)
					
			elif(input_parameter == 'density'):
				D = ReadField('D',I,input_dir,Version,iMax,jMax,kMax)
				D = D.astype(numpy.float)
				if(view_plane == 'XZ' or view_plane == 'ZX'):
					Data = ((D[:,J,:]**2)**0.5).reshape(iMax-1, kMax-1)
				elif(view_plane == 'XY' or view_plane == 'YX'):
					Data = ((D[:,:,J]**2)**0.5).reshape(iMax-1, jMax-1)
				elif(view_plane == 'YZ' or view_plane == 'ZY'):
					Data = ((D[J,:,:]**2)**0.5).reshape(jMax-1, kMax-1)
					
			elif(input_parameter == 'temperature'):
				T = ReadField('T',I,input_dir,Version,iMax,jMax,kMax)
				T = T.astype(numpy.float)
				if(view_plane == 'XZ' or view_plane == 'ZX'):
					Data = ((T[:,J,:]**2)**0.5).reshape(iMax-1, kMax-1)
				elif(view_plane == 'XY' or view_plane == 'YX'):
					Data = ((T[:,:,J]**2)**0.5).reshape(iMax-1, jMax-1)
				elif(view_plane == 'YZ' or view_plane == 'ZY'):
					Data = ((T[J,:,:]**2)**0.5).reshape(jMax-1, kMax-1)			
			
			counter = counter + 1
			if(plot_type == 'contour'):
				output_file = CreateGnuplot(job_name, X, Y, Data, iMax, jMax, kMax, I, counter, input_parameter, view_plane, plot_type)
			elif(plot_type == 'vector' and input_parameter == 'velocity'):
				output_file = CreateVectorGnuplot(job_name, X, Y, U, V, W, Data, iMax, jMax, kMax, I, counter, input_parameter, view_plane, plot_type)
	elif(output_format == 'contour_image'):
		
		#frame_number = int(Skip)
		frame_number = ETime
		#print frame_number
		#plottinDataManipulation(job_name, input_dir,grid_file,Version,STime,Skip,ETime,iMax,jMax,kMax,J,NContour, input_parameter, view_plane, output_format, frame_number)
		if(input_parameter == 'velocity'):
			u=ReadField('u',frame_number,input_dir,Version,iMax,jMax,kMax)
			v=ReadField('v',frame_number,input_dir,Version,iMax,jMax,kMax)
			w=ReadField('w',frame_number,input_dir,Version,iMax,jMax,kMax)
			################################
			[uc, vc, wc] = VecToCenter(u,v,w,iMax,jMax,kMax)
			################################
			if(view_plane == 'XZ' or view_plane == 'ZX'):
				Data = (((uc[:,J,:]**2) + (vc[:,J,:]**2) + (wc[:,J,:]**2))**0.5).reshape(iMax-1, kMax-1)
				U = uc[:,J,:].reshape(iMax-1, kMax-1)
				V = vc[:,J,:].reshape(iMax-1, kMax-1)
				W = wc[:,J,:].reshape(iMax-1, kMax-1)
			elif(view_plane == 'XY' or view_plane == 'YX'):
				Data = (((uc[:,:,J]**2) + (vc[:,:,J]**2) + (wc[:,:,J]**2))**0.5).reshape(iMax-1, jMax-1)
				U = uc[:,:,J].reshape(iMax-1, jMax-1)
				V = vc[:,:,J].reshape(iMax-1, jMax-1)
				W = wc[:,:,J].reshape(iMax-1, jMax-1)
			elif(view_plane == 'YZ' or view_plane == 'ZY'):
				Data = (((uc[J,:,:]**2) + (vc[J,:,:]**2) + (wc[J,:,:]**2))**0.5).reshape(jMax-1, kMax-1)
				U = uc[J,:,:].reshape(jMax-1, kMax-1)
				V = vc[J,:,:].reshape(jMax-1, kMax-1)
				W = wc[J,:,:].reshape(jMax-1, kMax-1)
					
		elif(input_parameter == 'pressure'):
			p = ReadField('p',frame_number,input_dir,Version,iMax,jMax,kMax)
			p = p.astype(numpy.float)
			if(view_plane == 'XZ' or view_plane == 'ZX'):
				Data = ((p[:,J,:]**2)**0.5).reshape(iMax-1, kMax-1)
			elif(view_plane == 'XY' or view_plane == 'YX'):
				Data = ((p[:,:,J]**2)**0.5).reshape(iMax-1, jMax-1)
			elif(view_plane == 'YZ' or view_plane == 'ZY'):
				Data = ((p[J,:,:]**2)**0.5).reshape(jMax-1, kMax-1)
				
		elif(input_parameter == 'density'):
			D = ReadField('D',frame_number,input_dir,Version,iMax,jMax,kMax)
			D = D.astype(numpy.float)
			if(view_plane == 'XZ' or view_plane == 'ZX'):
				Data = ((D[:,J,:]**2)**0.5).reshape(iMax-1, kMax-1)
			elif(view_plane == 'XY' or view_plane == 'YX'):
				Data = ((D[:,:,J]**2)**0.5).reshape(iMax-1, jMax-1)
			elif(view_plane == 'YZ' or view_plane == 'ZY'):
				Data = ((D[J,:,:]**2)**0.5).reshape(jMax-1, kMax-1)
				
		elif(input_parameter == 'temperature'):
			T = ReadField('T',frame_number,input_dir,Version,iMax,jMax,kMax)
			T = T.astype(numpy.float)
			if(view_plane == 'XZ' or view_plane == 'ZX'):
				Data = ((T[:,J,:]**2)**0.5).reshape(iMax-1, kMax-1)
			elif(view_plane == 'XY' or view_plane == 'YX'):
				Data = ((T[:,:,J]**2)**0.5).reshape(iMax-1, jMax-1)
			elif(view_plane == 'YZ' or view_plane == 'ZY'):
				Data = ((T[J,:,:]**2)**0.5).reshape(jMax-1, kMax-1)			
		
		if(plot_type == 'contour'):
			output_file = CreateGnuplot(job_name, X, Y, Data, iMax, jMax, kMax, frame_number, frame_number, input_parameter, view_plane, plot_type)
		elif(plot_type == 'vector' and input_parameter == 'velocity'):
			output_file = CreateVectorGnuplot(job_name, X, Y, U, V, W, Data, iMax, jMax, kMax, frame_number, frame_number, input_parameter, view_plane, plot_type)
		#output_file = CreateGnuplot(job_name, X, Y, Data, iMax, jMax, kMax, frame_number, frame_number, input_parameter, view_plane)
	return output_file

def CreateMovie(job_name, input_parameter, view_plane, plot_type):
	"""encoder = os.system("which ffmpeg")
	print encoder
	if(len(encoder) == 0):
		feedback['error'] = 'true'
		feedback['message'] = ('ERROR: Movie create encoder not found')
		print feedback
		return
	"""
	movie_name = job_name + '_' + input_parameter+ '_' + view_plane + '_'+ plot_type + "_movie.mp4"
	cmd = "ffmpeg -qscale 1 -r 3 -b 3000k -i " + input_parameter + '_' + view_plane + '_'+ plot_type + "_image_%01d.png " + movie_name;
	print cmd
	os.system(cmd)
	return movie_name

def CreateVectorGnuplot(job_name, X, Y, U, V, W, Data, iMax, jMax, kMax, I, counter, input_parameter, view_plane, plot_type):
	gnuplot_grid_file = job_name.split('.dat', 1)
	filename = gnuplot_grid_file[0] + str(I) + '_' + input_parameter + '_' + view_plane +'_contour_grid.dat'
	filename_vector = gnuplot_grid_file[0] + str(I) + '_' + input_parameter + '_' + view_plane +'_contour_grid_vector.dat'
	
	try:
		FILE_contour = open(filename,"w")
		FILE_vectour = open(filename_vector,"w")
	except Exception as e:
		feedback['error'] = 'true'
		feedback['message'] = ('ERROR: %s' % e)
		print feedback
		return
	# creating gnuplot compatible data file for ploting bathymetry
	if(view_plane == 'XZ' or view_plane == 'ZX'):
		for i in range(0, iMax-2):
			for j in range(0, kMax-2):
				FILE_contour.write("%f %f %f\n" % (X[i][j], Y[i][j], Data[i][j]))
				FILE_vectour.write("%f %f %f %f\n" % (X[i][j], Y[i][j], (X[i+1][j+1] - X[i][j]), (Y[i+1][j+1] - Y[i][j])))
			FILE_contour.write("\n")
			FILE_vectour.write("\n")
	elif(view_plane == 'XY' or view_plane == 'YX'):
		for i in range(0, iMax-1):
			for j in range(0, jMax-1):
				FILE_contour.write("%f %f %f\n" % (X[i][j], Y[i][j], Data[i][j]))
				FILE_vectour.write("%f %f %f %f\n" % (X[i][j], Y[i][j], Data[i][j], Data[i][j]))
			FILE_contour.write("\n")
			FILE_vectour.write("\n")
	elif(view_plane == 'YZ' or view_plane == 'ZY'):
		for i in range(0, jMax-1):
			for j in range(0, kMax-1):
				FILE_contour.write("%f %f %f\n" % (X[i][j], Y[i][j], Data[i][j]))
				FILE_vectour.write("%f %f %f %f\n" % (X[i][j], Y[i][j], Data[i][j], Data[i][j]))
			FILE_contour.write("\n")
			FILE_vectour.write("\n")
	

	plot_filename = input_parameter + '_' + view_plane + '_'+ plot_type + "_image_" + str(counter) + ".png"
	table_name = gnuplot_grid_file[0] + str(I) + '_' + input_parameter + '_' + view_plane +'_contour_grid_table.tmp'
	
	g = Gnuplot.Gnuplot(debug=1)
	g('    ')
	temp = g.clear()
	g('    ')
	title = "2D Vector Plot. Step Interval: %i" % (counter) 
	temp = g.title(title)
	g('    ')
	temp = g('set samples 40')
	g('    ')
	temp = g('set isosamples 21')
	g('    ')
	temp = g('set cntrparam levels 20')
	g('    ')
	#temp = g('set palette rgbformulae 23,28,3')
	g('    ')
	temp = g('set contour')
	g('    ')
	temp = g('unset clabel')
	g('    ')
	temp = g('unset surface')
	g('    ')
	temp = g('unset key')
	g('    ')
	temp = g('set view 0, 0')
	g('    ')
	""" PREVIOUS WORKING CODE ON LOCALHOST"""
	cmd = 'set table "%s"' % (table_name)
	g('    ')
	temp = g(cmd)
	g('    ')
	temp = g.splot(Gnuplot.File(filename, with_='lines'))
	g('    ')
	temp = g('unset table')
	
	"""
	temp = g('set terminal table')
	g('    ')
	cmd = 'set output "%s"' % (table_name)
	g('    ')
	temp = g(cmd)
	"""
	
	g('    ')
	#temp = g('set palette defined (0 "#668D3C", 1 "#404F24", 2 "#F5B22A", 3 "#10444C")')
	#g('    ')
	temp = g.splot(Gnuplot.File(filename, with_='lines'))
	g('    ')
	#temp = g('set terminal png')
	#g('    ')
	#cmd = 'set output "%s"' % (plot_filename)
	#temp = g('set style arrow 3 head filled size screen 0.03,15,45 ls 1')
	g('    ')
	temp = g.plot(Gnuplot.File(filename_vector, with_='vec', every ='4:4', using='1:2:3:4'), Gnuplot.File(table_name, with_='lines lc rgb "#000000"'))
	#temp = g.plot(Gnuplot.File(table_name, with_='vec'), Gnuplot.File(filename, with_='lines lc rgb "#000000"'))
	g('    ')
	temp = g.hardcopy(plot_filename, terminal='png')
	g('    ')	
	#save file name in global list
	outputfile_list.append(plot_filename)
	return plot_filename

def CreateGnuplot(job_name, X, Y, Data, iMax, jMax, kMax, I, counter, input_parameter, view_plane, plot_type):
	gnuplot_grid_file = job_name.split('.dat', 1)
	filename = gnuplot_grid_file[0] + str(I) + '_' + input_parameter + '_' + view_plane +'_contour_grid.dat'
	
	try:
		FILE = open(filename,"w")
	except Exception as e:
		feedback['error'] = 'true'
		feedback['message'] = ('ERROR: %s' % e)
		print feedback
		return
	# creating gnuplot compatible data file for ploting bathymetry
	if(view_plane == 'XZ' or view_plane == 'ZX'):
		for i in range(0, iMax-1):
			for j in range(0, kMax-1):
				FILE.write("%f %f %f\n" % (X[i][j], Y[i][j], Data[i][j]))
			FILE.write("\n")
	elif(view_plane == 'XY' or view_plane == 'YX'):
		for i in range(0, iMax-1):
			for j in range(0, jMax-1):
				FILE.write("%f %f %f\n" % (X[i][j], Y[i][j], Data[i][j]))
			FILE.write("\n")
	elif(view_plane == 'YZ' or view_plane == 'ZY'):
		for i in range(0, kMax-1):
			for j in range(0, jMax-1):
				FILE.write("%f %f %f\n" % (X[i][j], Y[i][j], Data[i][j]))
			FILE.write("\n")
	

	plot_filename = input_parameter + '_' + view_plane + '_'+ plot_type + "_image_" + str(counter) + ".png"
	
	g = Gnuplot.Gnuplot(debug=0)
	g('    ')
	temp = g.clear()
	g('    ')
	title = "2D Contour Plot. Step Interval: %i" % (counter) 
	temp = g.title(title)
	g('    ')
	temp = g('set samples 40')
	g('    ')
	temp = g('set isosamples 21')
	g('    ')
	temp = g('set view 0, 0')
	g('    ')
	temp = g('set xlabel "X"')
	g('    ')
	temp = g('set ylabel "Y"')
	g('    ')
	temp = g('set zlabel "Z"')
	g('    ')
	#temp = g('set palette rgb 33,13,10; set title "rainbow (blue-green-yellow-red)')
	#temp = g('set palette model HSV rgbformulae 3,2,2')
	#temp = g('set pm3d at sb')
	temp = g('set cntrparam levels 20')
	g('    ')
	temp = g('set contour')
	g('    ')
	temp = g('unset clabel')
	g('    ')
	temp = g('set nosurface')
	g('    ')
	temp = g('unset key')
	g('    ')
	#temp = g('set view 50, 300')
	#temp = g('set palette defined (0 "#668D3C", 1 "#404F24", 2 "#F5B22A", 3 "#10444C")')
	temp = g('set palette rgbformulae 23,28,3')
	g('    ')
	temp = g.splot(Gnuplot.File(filename, with_='lines'))
	g('    ')
	temp = g.hardcopy(plot_filename, terminal='png')
	g('    ')
	#save file name in global list
	outputfile_list.append(plot_filename)
	
	return plot_filename

def VecToCenter(u,v,w,iMax,jMax,kMax):
	uc = numpy.zeros((iMax-1,jMax-1,kMax-1))
	vc = numpy.zeros((iMax-1,jMax-1,kMax-1))
	wc = numpy.zeros((iMax-1,jMax-1,kMax-1))
	u = u.astype(numpy.float)
	v = v.astype(numpy.float)
	w = w.astype(numpy.float)	
	
	for k in range(0, (kMax-1)):
		for j in range(0, (jMax-1)):
			for i in range(0, (iMax-1)):
				uc[i][j][k]= u[i+1][j][k] + u[i][j][k]
				vc[i][j][k]= v[i][j+1][k] + v[i][j][k]
				wc[i][j][k]= w[i][j][k+1] + w[i][j][k]

	uc = uc*0.5
	vc = vc*0.5
	wc = wc*0.5		
	return (uc, vc, wc)
	
def PressureToCenter(p,iMax,jMax,kMax):
	up = numpy.zeros((iMax-1,jMax-1,kMax-1))
	p = p.astype(numpy.float)	
	
	for k in range(0, (kMax-1)):
		for j in range(0, (jMax-1)):
			for i in range(0, (iMax-1)):
				up[i][j][k]= p[i+1][j][k] + p[i][j][k]


	up = up*0.5	
	return (up)

def CalCenter(X, Y, Z, iMax,jMax,kMax):
	Xc = [ [ [ 0.000000 for k in range(kMax-1)] for j in range(jMax-1)] for i in range(iMax-1)]
	Yc = [ [ [ 0.000000 for k in range(kMax-1)] for j in range(jMax-1)] for i in range(iMax-1)]
	Zc = [ [ [ 0.000000 for k in range(kMax-1)] for j in range(jMax-1)] for i in range(iMax-1)]	
	
	X = numpy.array(X)
	Y = numpy.array(Y)
	Z = numpy.array(Z)
	X = X.astype(numpy.float)
	Y = Y.astype(numpy.float)
	Z = Z.astype(numpy.float)
	
	try:
		for i in range(0, iMax-1):
			for j in range(0, jMax-1):
				for k in range(0, kMax-1):
					Xc[i][j][k] = (X[i][j][k]+X[i+1][j][k]+X[i][j+1][k]+X[i+1][j+1][k]+X[i][j][k+1]+X[i+1][j][k+1]+X[i][j+1][k+1]+X[i+1][j+1][k+1])
					Yc[i][j][k] = (Y[i][j][k]+Y[i+1][j][k]+Y[i][j+1][k]+Y[i+1][j+1][k]+Y[i][j][k+1]+Y[i+1][j][k+1]+Y[i][j+1][k+1]+Y[i+1][j+1][k+1])
					Zc[i][j][k] = (Z[i][j][k]+Z[i+1][j][k]+Z[i][j+1][k]+Z[i+1][j+1][k]+Z[i][j][k+1]+Z[i+1][j][k+1]+Z[i][j+1][k+1]+Z[i+1][j+1][k+1])
	except Exception as e:
		feedback['error'] = 'true'
		feedback['message'] = ('ERROR: %s' % e)
		print feedback
		return
	#newList = [x/myInt for x in myList]
	Xc = numpy.array(Xc)
	Yc = numpy.array(Yc)
	Zc = numpy.array(Zc)
	Xc = Xc/8.0
	Yc = Yc/8.0
	Zc = Zc/8.0
		
	return (Xc, Yc, Zc)	


def ReadField(c, i, input_dir, Version, iMax, jMax, kMax):
	FileNum = GetFileNum(i,Version)
	fn = ''.join([input_dir, '/', c])
	if(int(Version) == 0):
		ResFile = ''.join([fn, FileNum])
		fileHandler = open(ResFile)
		fileData = fileHandler.read()
		fileDataArray = fileData.split('\n')		
		fileDataArray = [map(float, v) for v in fileDataArray]	
		fileDataArray = numpy.array(fileDataArray)
		fileDataArray = numpy.delete(fileDataArray, (fileDataArray.size-1), 0)
		if(c == 'u'):
			Result = fileDataArray.reshape(iMax, jMax-1, kMax-1)
		elif(c == 'v'):
			Result = fileDataArray.reshape(iMax-1, jMax, kMax-1)
		elif(c == 'w'):
			Result = fileDataArray.reshape(iMax-1,jMax-1, kMax)
		elif(c == 'p'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		elif(c == 'T'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		elif(c == 'S'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		elif(c == 'D'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		else:
			print "ERROR"
	elif(int(Version)==1):
		ResFile = ''.join([fn, '_', FileNum])
		fileHandler = open(ResFile)
		fileData = fileHandler.read()
		fileDataArray = fileData.split('\n')
		fileDataArray = numpy.array(fileDataArray)
		fileDataArray = numpy.delete(fileDataArray, (fileDataArray.size-1), 0)
		if(c == 'u'):
			Result = fileDataArray.reshape(iMax, jMax-1, kMax-1)
		elif(c == 'v'):
			Result = fileDataArray.reshape(iMax-1, jMax, kMax-1)
		elif(c == 'w'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax)
		elif(c == 'p'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		elif(c == 'T'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		elif(c == 'S'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		elif(c == 'D'):
			Result = fileDataArray.reshape(iMax-1, jMax-1, kMax-1)
		else:
			print "ERROR"
	else:
		ResFile = ''.join([fn, FileNum])
		fileHandler = open(ResFile)
		fileData = fileHandler.read()
		fileDataArray = fileData.split('\n')
		fileDataArray = numpy.array(fileDataArray)
		fileDataArray = numpy.delete(fileDataArray, (fileDataArray.size-1), 0)
    	if(c == 'u'):
    		Result = numpy.reshape(fileDataArray, (iMax, jMax-1, kMax-1), order= 'F')
    	elif(c == 'v'):
    		Result = numpy.reshape(fileDataArray, (iMax-1, jMax, kMax-1), order= 'F')
    	elif(c == 'w'):
    		Result = numpy.reshape(fileDataArray, (iMax-1, jMax-1, kMax), order= 'F')
    	elif(c == 'p'):
    		Result = numpy.reshape(fileDataArray, (iMax-1, jMax-1, kMax-1), order= 'F')
    	elif(c == 'T'):
    		Result = numpy.reshape(fileDataArray, (iMax-1, jMax-1, kMax-1), order= 'F')
    	elif(c == 'S'):
    		Result = numpy.reshape(fileDataArray, (iMax-1, jMax-1, kMax-1), order= 'F')
    	elif(c == 'D'):
    		Result = numpy.reshape(fileDataArray, (iMax-1, jMax-1, kMax-1), order= 'F')
    	else:
    		print "ERROR"
	
	return Result

def GetFileNum(i,Version):
	if(int(Version) == 1):
		if(int(i)<10):
			FileNum = ''.join(['00000', str(i), '.dat'])
		elif(int(i)<100):
			FileNum=''.join(['0000', str(i), '.dat'])
		elif(int(i)<1000):
			FileNum=''.join(['000', str(i), '.dat'])
		elif(int(i)<1000):
			FileNum=''.join(['00', str(i), '.dat'])
		elif(int(i)<100000):
			FileNum=''.join(['0', str(i), '.dat'])
		else:
			FileNum=''.join([str(i), '.dat'])
	else:
		if(int(i)<10):
			FileNum=''.join(['000', str(i), '.dat'])         
		elif(int(i)<100):
			FileNum=''.join(['00', str(i), '.dat'])
		elif(int(i)<1000):
			FileNum=''.join(['0', str(i), '.dat'])
		else:
			FileNum=''.join([str(i), '.dat'])
	return FileNum


if __name__ == '__main__':
	main()