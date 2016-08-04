This file is for you to describe the cyberweb application. Typically
you would include information such as the information below:

Installation and Setup
======================

Part I: Basic Installation 
Part II:  Detailed Notes
Part III: Code dependencies



Part I: Basic Installation 
1. Download cyberweb:
    % co http://acel.sdsu.edu/trac/cyberweb/browser/trunk/development.db

2. Installation: 
   Get easy_install:

3. If needed, modify the startup database

   Remove old development.db (or other db) file	
   Edit data file: initial_data.json 
       
4. Update the database

   Run:
   % paster setup-app development.ini

   watch for startup errors, fix, and rerun.

5. Modify global variables defined in development.ini
# Configure various host and path information needed at startup
	cw.timeout             = 5  # Timeout user sessions in minutes
	cw.home_dir            = %(here)s
	
# Configure remote resource directories

Part II:  Detailed Notes


Part III: Code dependencies
1. easy_install

**************************************************
            IS THIS RELEVANT?
*************************************************

Install ``cyberweb`` using easy_install::


Make a config file as follows::

    paster make-config cyberweb config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
