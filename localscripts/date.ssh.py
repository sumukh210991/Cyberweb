#! /usr/bin/env python
import os
import sys
from subprocess import Popen,PIPE

l = len(sys.argv)
if l == 2 :
   if sys.argv[1] :
      cwhost = sys.argv[1].strip()
   else :
      print 'ERROR: Missing HostName.'
      sys.exit()
else:
   print ('ERROR:  Not enough args: len = %s' % l)
   sys.exit()

out=''
if cwhost.find( "babilonia") > -1 :
   out = "babilonia connection not authorized for demo modes."
   out2  = Popen(['nslookup','babilonia.facyt.uc.edu.ve' ],stdout=PIPE).communicate()[0]
   out = out + '\n' + out2
else:
   sshcmd = '/usr/bin/ssh'
   out  = Popen([sshcmd,cwhost,'hostname; whoami; /bin/date '],stdout=PIPE).communicate()[0]

print out


