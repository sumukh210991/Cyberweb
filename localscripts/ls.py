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

if not len(hosts):
    print 'No hostname found.'
    sys.exit(0)

for host in hosts:
    mycmd = '/usr/local/globus4.2.1/bin/gsissh'
    myarg = host
    #myarg = 'tg-login.ncsa.teragrid.org'
    mycmdarg1 = "/bin/ls"
    mycmdarg2 = "-al"
    mycmdarg3 = "/usr"
    output = Popen([mycmd,myarg,mycmdarg1,mycmdarg2,mycmdarg3],stdout=PIPE).communicate()[0]
    #output = Popen([mycmd,myarg,"/bin/ls","/"],stdout=PIPE).communicate()[0]
    print output

