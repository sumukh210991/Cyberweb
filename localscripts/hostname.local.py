#! /usr/bin/env python
#####
#  test code for connecting to teragrid usin gsissh
###
import os
import sys

from subprocess import *
mycmd='hostname;date'
output = Popen([mycmd], stdout=PIPE).communicate()[0]
print output

