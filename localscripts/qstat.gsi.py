#! /usr/bin/env python
#
#####
#  test code for connecting to teragrid usin gsissh
###
import os
import sys
from subprocess import Popen,PIPE

ldp = os.environ['LD_LIBRARY_PATH']
print 'LD_LIBRARY_PATH: ' + ldp
l=len(sys.argv)
print ('number of args=%s'  % l)
i=0
while (i < l):
    print ('sys.argv[%s]=%s' % (i,sys.argv[i]))
    i=i+1

if (len(sys.argv) >= 3):
    X509_USER_PROXY  = sys.argv[1].strip()
    hostname = sys.argv[2].strip()
    GLOBUS_LOCATION = '/usr/local/globus-5.0.2'
    os.environ['GLOBUS_LOCATION'] = GLOBUS_LOCATION
    os.environ['X509_USER_PROXY'] = X509_USER_PROXY
    os.environ['LD_LIBRARY_PATH'] = GLOBUS_LOCATION + '/lib' 
    gsicmd = GLOBUS_LOCATION + '/bin/gsissh'
    print( 'GSI_CMD: %s %s %s ' % ( gsicmd, hostname, 'qstat a') )

    try:
       out1 = Popen([gsicmd,hostname,'whoami; hostname; qstat -a'],stdout=PIPE).communicate()[0]
       print ("CONNECTION 1: %s " % out1)
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except ValueError:
        print "Could not convert data to an integer."
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

##    except:
##       print 'GSI_CMD: problem with gsicommand: ', gsicmd
else:
    print ('ERROR: Not enough arguments: %s ' % len(sys.argv) )
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
print 'os.environ: [[[[[[[[[[[[[[[[[[[[' ,  os.environ,']]]]]]]]]]]]]]]]]]'
sys.exit()

