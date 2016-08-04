"""Setup the cyberweb application"""
import logging
import os

import pylons.test
from pylons import config

from cyberweb.config.environment import load_environment
from cyberweb.model.meta import Session, Base
from cyberweb import model

import simplejson as json
import types

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup cyberweb here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)


    # Wait until we load the environment before we can load the encryption
    # algorithm from the authkit.
    myclass, myfunc = config.get('authkit.form.authenticate.user.encrypt',':').split(':')
    mysecret = config.get('authkit.form.authenticate.user.encrypt.secret','')
    try: exec('from %s import %s as encrypt' % (myclass,myfunc))
    except: encrypt = lambda x,y: x

    # Drop the tables if they exist
    #log.info("Dropping database tables...")
    #Base.metadata.drop_all(bind=Session.bind)
    # Create the tables if they don't already exist
    log.info("Creating database tables...")
    Base.metadata.create_all(bind=Session.bind)

    # Load an initial database from a JSON file
    log.info("Populating initial data...")
    datafile = 'initial_data.json'
    if (os.path.isfile(datafile)):
        log.info("Loading initial data from file(%s)" % datafile)
        try:
            for i in json.load(open(datafile,'r')):
                print i.get('model')
                mymodel = eval('%s()' % i.get('model'))
                # Import data items
                username = 'Unknown'
                for k,v in i.get('fields').items():
                    if isinstance(v,types.StringType):
                        exec('mymodel.%s = \'%s\'' % (k,v))
                    elif isinstance(v,types.UnicodeType):
                        exec('mymodel.%s = \'%s\'' % (k,v.encode()))
                    elif isinstance(v,types.IntType):
                        exec('mymodel.%s = %d' % (k,v))
                    elif isinstance(v,types.FloatType):
                        exec('mymodel.%s = %f' % (k,v))
                    else:
                        log.debug('Unknown type for mymodel.%s: %s' % (k,v.__class__))

                Session.add(mymodel)
                try: Session.commit()
                except Exception, e:
                    Session.remove()
                    log.warn('Failed insertion into %s. Skipping: %s' % (i.get('model'),e.message))
            log.info('Finished importing json file.')
        except Exception:
            log.error('failed importing into database: ')
            Session.remove()
        else:
            log.info("CyberWeb database successfully set up.")
            m1 = model.Message(1,0,'You have successfully installed CyberWeb.')
            m2 = model.Message(1,0,'Welcome to CyberWeb.')
            try:
                Session.add(m1)
                Session.add(m2)
                Session.commit()
            except:
                pass

    Session.close()