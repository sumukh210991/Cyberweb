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

class Gccom:
    # Eventually, this is pulled from the database
    gccom_comm_acct = ''
    gcem_dir        = 'GCEMproj'
    gccom_dir       = 'gccom'

    #set up names of and parameter data. configuration status == 0/1 == y/n
    #note: eventually will use this to list all grids, select one, and print an image of the grid.
    # note: for temps (ldc1, ldc2),  boxgrid.dat and grid.dat are same.
    bath_grid = {
          'hdrs'         : {  'name':'Grid Name','IMax':0,'JMax':0,'KMax':0,'img':'Image File','desc':'Description',
                               'fname':'filename'},
          'cube-box'     : {  'name':'Cube Box','IMax':32,'JMax':32,'KMax':32,'img':'gridbox',
                              'desc':'Cube Grid Box for test cases tests',
                               'fname':'grid.32x32x32.dat'},
          'long-box'     : {  'name': 'Long Box','IMax':33,'JMax':33,'KMax':97,'img':'long-box',
                              'desc':'Long Box for test cases tests',
                               'fname':'longboxgrid.33x33x97.dat'},
          'seamount'     : {  'name':'Simple Seamount','IMax':97,'JMax':33,'KMax':33,'img':'seamount',
                              'desc':'Simple Seamount description',
                               'fname':'Seamount.97x33x33.dat'},
          'channel'      : {  'name':'Channel','IMax':0,'JMax':0,'KMax':0,'img':'channel',
                              'desc':'Channel Box for test cases tests',
                               'fname':'filename'},
          'montbay'      : {  'name':'MontereyBay','IMax':0,'JMax':0,'KMax':0,'img':'image',
                              'desc':'description',
                               'fname':'filename'},
          }
    ## note: there is aproblem here in that i am hardcoding elements in exec code. 
    ## need to move to looking at header, mathching index of key and then using that.
    model_info = {
          'hdrs'         : { 'desc'      :'Description', 
                             'st'        :'status',
                             'modeldir'  :'execdir',
                             'modelname' :'modelname',
                             'grid_key'  :'grid_key' 
                           },
          'ldc1'         : { 'desc'      :'Lid Driven Cavity Test Case 1', 
                             'st'        : 0, 
                             'modeldir'  :'cwproj/gccom/ldc1',
                             'modelname' :'gccom.ldc1',
                             'grid_key'  :'cube-box'  
                           },
          'ldc2'         : { 'desc'      :'Lid Driven Cavity Test Case 2', 
                              'st'       : 1, 
                             'modeldir'  :'cwproj/gccom/ldc2',
                             'modelname' :'gccom.ldc2',
                             'grid_key'  :'cube-box'  
                           },
          'temperature1' : { 'desc'      :'Temperature Test Case 1', 
                             'st'        : 1 , 
                             'modeldir'  :'cwproj/gccom/temperature1',
                             'modelname' :'gccom.temperature1',
                             'grid_key'  :'cube-box' 
                           },
          'temperature2' : { 'desc'      :'Temperature Test Case 2', 
                             'st'        : 1, 
                             'modeldir'  :'cwproj/gccom/temperature2',
                             'modelname' :'gccom.temperature2' ,
                             'grid_key'  :'long-box' 
                           },
          'seamount1'    : { 'desc'      :'Simple Seamount Test Case 1', 
                             'st'        : 1, 
                             'modeldir'  :'cwproj/gccom/seamount1',
                             'modelname' :'gccom.seamount1' ,
                             'grid_key'  :'seamount' 
                           },
          } 
    model_params = {
          'hdrs' : [ 'Parameter','Description','Value' ],
          'ldc2' : [
                     ['IterM','Max Iteration','100.000'],
                     ['dt','Time Step (dt)','0.0001'],
                     ['MaxFileNo','Max File No','10.000'],
                     ['wrthz','Writeout freq.','10.00'],
                     ['omp','Omega Pres.','1.0'],
                     ['epsp','eps. Pres.','0.0000001'],
                     ['itemp','SOR Max Iter P.','5000.0'],
                     ['Re','Reynolds Number','1000.0'],
                     ['PrT','PrT  Number','5.0'],
                     ['PrS','PrS  Number','5.0'],
                     ['Ros','Rossby Number','0.0'],
                     ['Fr','Froud Number','0.003'],
                     ['UStar','Velocity Scale','0.1'],
                     ['LStar','Length Scale','1.0'],
                     ['TStar','Temp. Scale','40.0'],
                     ['SStar','Salinity Scale','42.0'],

                ],
          'seamount1' : [
                     ['IterM','Max Iteration','100.000'],
                     ['dt','Time Step (dt)','0.0001'],
                     ['MaxFileNo','Max File No','10.000'],
                     ['wrthz','Writeout freq.','10.00'],
                     ['omp','Omega Pres.','1.0'],
                     ['epsp','eps. Pres.','0.0000001'],
                     ['itemp','SOR Max Iter P.','5000.0'],
                     ['Re','Reynolds Number','1000.0'],
                     ['PrT','PrT  Number','5.0'],
                     ['PrS','PrS  Number','0.0'],
                     ['Ros','Rossby Number','0.0'],
                     ['Fr','Froud Number','0.00'],
                     ['UStar','Velocity Scale','0.1'],
                     ['LStar','Length Scale','1.0'],
                     ['TStar','Temp. Scale','10.0'],
                     ['SStar','Salinity Scale','42.0'],
                ],
          'temperature1' : [
                     ['IterM','Max Iteration','100.000'],
                     ['dt','Time Step (dt]','0.0001'],
                     ['MaxFileNo','Max File No','10.000'],
                     ['wrthz','Writeout freq.','10.00'],
                     ['omp','Omega Pres.','1.0'],
                     ['epsp','eps. Pres.','0.0000001'],
                     ['itemp','SOR Max Iter P.','1000.0'],
                     ['Re','Reynolds Number','1000.0'],
                     ['PrT','PrT  Number','5.0'],
                     ['PrS','PrS  Number','5.0'],
                     ['Ros','Rossby Number','0.0'],
                     ['Fr','Froud Number','0.003'],
                     ['UStar','Velocity Scale','0.1'],
                     ['LStar','Length Scale','1.0'],
                     ['TStar','Temp. Scale','10.0'],
                     ['SStar','Salinity Scale','42.0'],
                ],
          'temperature2' : [
                     ['IterM','Max Iteration','100.000'],
                     ['dt','Time Step (dt]','0.0001'],
                     ['MaxFileNo','Max File No','10.000'],
                     ['wrthz','Writeout freq.','10.00'],
                     ['omp','Omega Pres.','1.0'],
                     ['epsp','eps. Pres.','0.0000001'],
                     ['itemp','SOR Max Iter P.','5000.0'],
                     ['Re','Reynolds Number','1000.0'],
                     ['PrT','PrT  Number','5.0'],
                     ['PrS','PrS  Number','0.0'],
                     ['Ros','Rossby Number','0.0'],
                     ['Fr','Froud Number','1.00'],
                     ['UStar','Velocity Scale','0.1'],
                     ['LStar','Length Scale','1.0'],
                     ['TStar','Temp. Scale','10.0'],
                     ['SStar','Salinity Scale','42.0'],
                ],
       }

    def __init__(self):
        # Resource list will eventually be pulled from database
        # @todo: Need to define the parameter list and grid files for each application.
        iccom_comm_acct = 'mary'
