#!/usr/bin/python
import os
import sys
from subprocess import Popen,PIPE
import subprocess

def main():
    feedback = {'error'     : 'false',
                'message'    : '',
                'parameters': ''
                }
    l = len(sys.argv)
    if l == 3 :
       if sys.argv[1] :
          cwhost = sys.argv[1].strip()
       else :
          print 'ERROR: Missing HostName.'
          sys.exit()
       if sys.argv[2] :
          path = sys.argv[2].strip()
       else :
          print 'ERROR: Missing HostName.'
          sys.exit()
    else:
       print ('ERROR:  Not enough args: len = %s' % l)
       sys.exit()
    
    
    try:
        proc = subprocess.Popen(["ls job.info.*"], stdout=subprocess.PIPE, shell=True)
        (filename, err) = proc.communicate()
        info_filename = filename.strip()
    except Exception as e:
        feedback['error'] = 'true'
        feedback['message'] = ('ERROR: %s' % e)
        print feedback
        return
    """
    try:
        path_folders = path.split('/')
        current_folder = path_folders[-1]
        folder_values = current_folder.split('_')
        ID = folder_values[-1]
    except Exception as e:
        feedback['error'] = 'true'
        feedback['message'] = "Job folder not in correct format. %s" % e
        print feedback
        return
    """
    #info_filename = 'job.info.%s' % ID
    out=''
    sshcmd = '/usr/bin/ssh'
    files=os.listdir(".")
    #ignore files starting with '.' using list comprehension
    files=[filename for filename in files if filename[0] != '.']
    try:
    	fd = open( info_filename, 'r')
    except Exception as e:
        feedback['error'] = 'true'
        feedback['message'] = "Job Info file not found. %s" % e
        print feedback
        return
    content = fd.readlines()
    for line in content:
    	#line = line.rstrip()
    	#line = ''.join([line, '<br />'])
    	feedback['message'] = feedback['message'] + line
    print feedback
    return


if __name__ == '__main__':
    main()