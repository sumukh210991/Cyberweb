import logging

from pylons import config, request, response, session, tmpl_context as c

from cyberweb import model
from cyberweb.model import meta

from datetime import datetime
from time import sleep

from threading import Thread
import paramiko

import jodis.sshresource as myssh
from time import sleep


log = logging.getLogger(__name__)

class Viz:
    # Eventually, this is pulled from the database
    
    #plotViews not in use yet
    plotViews = {'defaultView': 'Default View',
                 'dynamicView': 'Dynamic View'}
    
    dynamicViews = {'performance'  :   'Performance',
                   'dataType'     :   'Data Type'
                  }

	#{'name':'dataType'     , 'label'  :   'Data Type'			'subtype' : 'Data'},
    analysisTypes = ({'name':'performance'  , 'label'  :   'Performance',		'subtype' : 'Performance Type'},
    				{'name': 'contour'		, 'label'  :   '2D Contour', 			'subtype' : 'Contour Datatype'},
                    {'name':'bathymetry'   , 'label'  :   'Bathymetry Plots',    'subtype' : ''})
    
    #{'name': 'volume'        , 'label'  :   '3D Volume',             'subtype' : 'Volume Datatype'},
    #{'name': 'vector'        , 'label'  :   '2D Vector',             'subtype' : 'Vector Datatype'},
    
    performance = ({'name':'elapsedTime',    'label'    :'Run Time Plot'		, 'subtype' : ''},
                   {'name':'cumulativeTime', 'label'    :'Time Per Iteration'	, 'subtype' : ''}
                   )
    
    #{'name': 'runtime'     , 'label'  :   'Run Time Plot',        'subtype' : ''}
    
    dataTypes = ({'name':'velocityU',   'label':'Velocity U'},
                {'name':'velocityV',    'label':'Velocity V'},
                {'name':'velocityW',    'label':'Velocity W'},
                {'name':'velocityAvg',  'label':'Velocity Average'}
                )
    volume = ''
    elapsedTime = ''
    cumulativeTime = ''
    bathymetry = ''
    runtime = ''
    contour =  ({'name':'velocity', 'label':'Velocity'			, 'subtype' : 'Output Type'},
                {'name':'temperature', 'label':'Temperature'    , 'subtype' : 'Output Type'})
    """
    			{'name':'pressure', 'label':'Pressure'			, 'subtype' : 'Output Type'},
    			{'name':'density', 'label':'Density'			, 'subtype' : 'Output Type'},
    			)
    """
    
    				
    contour_output_format = ({'name' : 'contour_image', 'label' : 'Image'	, 'subtype' : 'Plane'},
    						{'name' : 'contour_movie', 'label' : 'Movie'	, 'subtype' : 'Plane'},
                            {'name' : 'contour_sequence', 'label' : 'Sequence Images'    , 'subtype' : 'Plane'})

    pressure = contour_output_format
    density = contour_output_format
    temperature = contour_output_format
    velocity = contour_output_format
    vector = contour_output_format
    
    plane = ({'name' : 'XY', 'label' : 'XY Plane (Top view)', 'subtype' : ''},
             {'name' : 'YZ', 'label' : 'YZ Plane (Side view)', 'subtype' : ''},
             {'name' : 'ZX', 'label' : 'ZX Plane (Front view)', 'subtype' : ''})
    
    contour_image = plane
    contour_movie = plane
    contour_sequence = plane
    
    XY = ''
    YZ = ''
    ZX = ''
    
    bathymetry_params = ({'name' : 'xmin',  'title' : 'X min',  'type' : 'int', 'value' : ''},
    					{'name' : 'xmax',  'title' : 'X max',  'type' : 'int', 'value' : ''},
    					{'name' : 'ymin',  'title' : 'Y min',  'type' : 'int', 'value' : ''},
    					{'name' : 'ymax',  'title' : 'Y max',  'type' : 'int', 'value' : ''},
    					{'name' : 'zmin',  'title' : 'Z min',  'type' : 'int', 'value' : ''},
    					{'name' : 'zmax',  'title' : 'Z max',  'type' : 'int', 'value' : ''},
    					{'name' : 'plot_type', 'title' : 'plot_type', 'type' : 'hidden', 'value' : 'bathymetry'},
    					{'name' : 'plot_file', 'title' : 'plot_file', 'type' : 'hidden', 'value' : ''})
    
    contour_params = ({'name' : 'skip_interval', 'title' : 'Skip Intervals', 'type' : 'int', 'value' : ''})
    					
    planes = ({'name' : 'XY' , 'title' : 'XY Plane'},
    		{'name' : 'YZ' , 'title' : 'YZ Plane'},
    		{'name' : 'ZX' , 'title' : 'ZX Plane'})
    
    contourMovie_params = ({'name' : 'plane', 'title' : 'Plane', 'type' : 'dropdown', 'value' : '', 'value_options' : planes})
    
    plots = {'plotViews'        : plotViews,
    		'dynamicView'      : dynamicViews,
    		'analysisTypes'    : analysisTypes,
    		'performance'      : performance,
    		'dataType'         : dataTypes,
    		'cumulativeTime'   : cumulativeTime,
    		'elapsedTime'      : elapsedTime,
    		'bathymetry'		: bathymetry,
    		'runtime'			: runtime,
    		'contour'			: contour,
    		'pressure'			: pressure,
    		'density'			: density,
    		'temperature'		: temperature,
    		'velocity'			: velocity,
    		'contour_image'		: contour_image,
    		'contour_movie'		: contour_movie,
            'contour_sequence'  : contour_sequence,
    		'contour_output_format': contour_output_format,
            'vector'            : vector,
            'plane'             : plane,
            'XY'                : XY,
            'YZ'                : YZ,
            'ZX'                : ZX,
            'volume'            : volume
    		}
    

    
    

    
    def __init__(self):
        # Resource list will eventually be pulled from database
        # @todo: Need to define the parameter list and grid files for each application.
         pass 

