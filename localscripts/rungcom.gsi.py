#! /usr/bin/env python
#####
#  test code for connecting to teragrid usin gsissh
###
import os
import sys
from subprocess import Popen,PIPE

hosts = []
for arg in sys.argv:
    arr = arg.split('=')
    if len(arr) == 2:
        if arr[0].strip() == 'host' or arr[0].strip() == 'hostname':
            hosts.append(arr[1].strip())
        elif arr[0].strip() == 'user' or arr[0].strip() == 'username':
            user = arr[1].strip()
        else:
            print '%s argument not supported yet.' % arr[0].strip()


#hostname = 'tg-login.ncsa.teragrid.org'
hostname = 'dolphin.sdsu.edu'
#username = 'thomasm'
cw_user = 'mary'
#cw_user = 'carny'

X509_USER_PROXY = "/home/carny/cyberweb/trunk/cw_user_data/%s/gsi/x509up_%s" % (cw_user,cw_user)
os.environ['X509_USER_PROXY'] = X509_USER_PROXY
print "X509: %s" % X509_USER_PROXY
 
mycmd = '/usr/local/globus4.2.1/bin/gsissh'
myarg = hostname  
gcomdir = "/home2/mthomas/CyberWeb/GCOM-NG" 
gcomcmd = "gcomnd"
mycmdarg1 = "cd /home2/mthomas/CyberWeb/GCOM-NG; ./gcomnd"
#mycmdarg1 = "cd CyberWeb/GCOM-NG; ls -al"
#mycmdarg1 = "cd CyberWeb/GCOM-NG; ./gcomndpgf"
#output = Popen([mycmd,myarg,mycmdarg1,mycmdarg2,mycmdarg3],stdout=PIPE).communicate()[0]
output = Popen([mycmd,myarg,mycmdarg1],stdout=PIPE).communicate()[0]
#output = Popen([mycmd,myarg,"/bin/ls","/"],stdout=PIPE).communicate()[0]
print output
for line in output.splitlines():
    arr = line.split()
    print arr
 

