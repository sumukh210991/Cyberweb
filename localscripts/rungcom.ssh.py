#! /usr/bin/env python
import os, commands
import sys
from subprocess import Popen,PIPE

l = len(sys.argv)
if l == 3 :
   if sys.argv[1] :
      cwhost = sys.argv[1].strip()
   else :
      print 'ERROR: Missing HostName.'   
      sys.exit()

   if sys.argv[2] :
      gc_model = sys.argv[2].strip()
   else :
      print 'ERROR: Missing Sript Name.'   
      sys.exit()
else:
   print ('ERROR:  Not enough args: len = %s' % l)
   sys.exit()

# this data should be passed as an argument from the controller....
hosts = {
          'dolphin' : '/nfs/dolphinfs/home4/carny/cwproj/gcom/mgcom.v5.ldc2' ,
          'anthill' :  '/home2/carny/cwproj/gcom/mgcom.v5.ldc2' ,
       }
gc_mdl_dirs = {
          'ldc'  : 'gcom-ng.r2.ldc',
          'buoy' : 'gcom-ng.r3.buoy',
         }

if 'dolphin' in cwhost :
   gc_home = hosts['dolphin']
else:
   gc_home = hosts['anthill']

gc_mdl_dir = gc_mdl_dirs[gc_model]

msg=''
#msg = msg + ('cwhost: %s \n ' % cwhost)
#msg = msg + ('gc_home: %s \n ' % gc_home)
#msg = msg + ('gc_mdl_dir: %s \n ' % gc_mdl_dir)
#msg = msg + ('gc_model: %s \n ' % gc_model)

#this test case works:
#gcmd = ( 'cd %s/%s ; hostname;  date ; whoami; pwd ' % (gc_home,gc_mdl_dir))
# this  works
gcmd = ( 'cd %s/%s ; hostname;  date ; whoami; pwd ; ./gcom-%s ' % (gc_home,gc_mdl_dir,gc_model))
#msg = msg + ('gcmd: %s \n ' % gcmd)

sshcmd = '/usr/bin/ssh'
# this test case works
#out = Popen([sshcmd,cwhost,'hostname; whoami; /bin/ls -al; '],stdout=PIPE).communicate()[0]
# this  works
out = Popen([sshcmd,cwhost, gcmd],stdout=PIPE).communicate()[0]

msg = msg + ('out: %s \n ' % out)

print msg 
#print err
#print output
#for line in output.splitlines():
#    arr = line.split()
#    print arr
 

