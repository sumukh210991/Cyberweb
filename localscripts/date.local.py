#! /usr/bin/env python
#####
import os
import sys
from subprocess import Popen,PIPE

output = Popen(['/bin/date'], stdout=PIPE).communicate()[0]
print output
