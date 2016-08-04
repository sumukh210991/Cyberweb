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


hostname = 'tg-login.ncsa.teragrid.org'
#username = 'thomasm'
cw_user = 'mary'
cw_user = 'carny'

X509_USER_PROXY = "/home/carny/cyberweb/trunk/cw_user_data/%s/gsi/x509up_%s" % (cw_user,cw_user)
os.environ['X509_USER_PROXY'] = X509_USER_PROXY
print "X509: %s" % X509_USER_PROXY
 
mycmd = '/usr/local/globus4.2.1/bin/gsissh'
myarg = hostname  
mycmdarg1 = "/bin/ls"
mycmdarg2 = "-al"
#output = Popen([mycmd,myarg,mycmdarg1,mycmdarg2,mycmdarg3],stdout=PIPE).communicate()[0]
output = Popen([mycmd,myarg,mycmdarg1,mycmdarg2],stdout=PIPE).communicate()[0]
#output = Popen([mycmd,myarg,"/bin/ls","/"],stdout=PIPE).communicate()[0]
print output
for line in output.splitlines():
    arr = line.split()
    print arr
 

