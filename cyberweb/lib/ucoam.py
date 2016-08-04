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

class Ucoam:
    # Eventually, this is pulled from the database
          
    ## note: there is aproblem here in that i am hardcoding elements in exec code. 
    ## need to move to looking at header, mathching index of key and then using that.
    model_info = {
          'hdrs'         : { 'desc':'Description', 'st':'status',
                             'appdir':'execdir','appname':'appname','grid_key':'grid_key' },
          'seamount'    : { 'desc':'Simple Seamount Test Case 1', 'st':1, 'appdir':'cwproj/ucoam/seamount',
                             'appname':'ucoam.seamount1' ,'grid_key':'seamount' },
          } 
       }

  #set up names of and parameter data. configuration status == 0/1 == y/n
    #note: eventually will use this to list all grids, select one, and print an image of the grid.
    bath_grid = {
          'hdrs'         : {  'name':'Grid Name','IMax':0,'JMax':0,'KMax':0,'img':'Image File','desc':'Description'},
          'cube-box'     : {  'name':'Cube Box','IMax':32,'JMax':32,'KMax':32,
                              'fname':'Grid2.32x32x32',  'img':'gridbox',
                              'desc':'Cube Grid Box for test cases tests'},
          'seamount'     : {  'name':'Seamount.97x33x33','IMax':97,'JMax':33,'KMax':33,'img':'seamount',
                              'fname':'',  'img':'gridbox',
                              'desc':'Simple Seamount description'},
          'alarcseamount'     : {  'name':'alarc.seamnt.out3840','IMax':41,'JMax':38,'KMax':38,'img':'',
                              'fname':'',  'img':'gridbox',
                              'desc':'Simple Seamount description'},
          'montbay'      : {  'name':'Monterey Bay','IMax':159,'JMax':59,'KMax':11,'img':'',
                              'fname':'MontereyBayGrid',  'img':'gridbox',
                              'desc':'description'},

    def __init__(self):
        # @todo: Need to define the parameter list and grid files for each application.
        pass
