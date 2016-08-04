"""The application's Globals object"""
import logging

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pylons import config as pyconfig

from cyberweb.lib.menu import MenuReader
from cyberweb.lib.helpers import getCWConfig
from cyberweb.model import meta, Account, User
from jodis import Jodis, Manager


log = logging.getLogger(__name__)


class Globals(object):
    """
    Globals acts as a container for objects available throughout the
    life of the application
    """
    jodis = None
    available_resources = {}
    menu = None

    def __init__(self, config):
        """
        One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable
        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        self.menu = MenuReader()
        self.cw_config = getCWConfig(config=config)
        self.cwusersdir = self.cw_config.get('user_dir')
        self.cwdatadir = self.cw_config.get('data_dir')

        ################################################
        # set up local (web server) directories
	## from dev. ini, remove after testing done.
	##cw.cwhome_loc          = %(here)s
	##cw.cwproj_loc          = %(cw.cwhome_loc)s/cwproj
	##cw.cwuser_loc          = %(cw.cwproj_loc)s/cwuser
	##cw.cwdata_loc          = %(cw.cwproj_loc)s/cwdata
	##cw.cwscripts_loc       = %(cw.cwproj_loc)s/cwscripts
	##cw.cwbath_loc          = %(cw.cwdata_loc)s/cwbath
	##cw.bathymetry_location = /home4/smita/bathymetry

        self.cwhome_loc = self.cw_config.get('home_loc')
        self.cwproj_loc = self.cw_config.get('proj_loc')
        self.cwuser_loc = self.cw_config.get('user_loc')
        self.cwdata_loc = self.cw_config.get('data_loc')
        self.cwscripts_loc = self.cw_config.get('scripts_loc')
        self.cwbath_loc = self.cw_config.get('bath_loc')

        ################################################
        # set up remote (web server) directories
	## from dev. ini, remove after testing done.
	# directories used by a cwproj service and its apps
	##cw.cwhome_rem          = CyberWeb
	##cw.cwproj_rem          = %(cw.cwhome_rem)s/cwproj.%(cw.dev_key)s
	##cw.cwuser_rem          = %(cw.cwproj_rem)s/cwuser
	##cw.cwdata_rem          = %(cw.cwproj_rem)s/cwdata
	##cw.cwscripts_rem       = %(cw.cwproj_rem)s/cwscripts

        self.cwhome_rem = self.cw_config.get('home_rem')
        self.cwproj_rem = self.cw_config.get('proj_rem')
        self.cwuser_rem = self.cw_config.get('user_rem')
        self.cwdata_rem = self.cw_config.get('data_rem')
        self.cwscripts_loc = self.cw_config.get('scripts_loc')

        projectname = self.cw_config.get('project.shortname', 'CyberWeb')
        projectfullname = self.cw_config.get('project.fullname', 'CyberWeb - A framework for Scienfic Applications')
        log.debug('GLOBALS INIT: project.fullname=[%s] ', self.cw_config.get('project.fullname'))
        self.title = pyconfig.get('project.title', projectfullname)

        log.debug('Loading cwusersdir: %s' % self.cwusersdir)
        log.debug('Loading cwdatadir: %s' % self.cwdatadir)
        log.debug('Loading project: %s' % projectname)
        if not Globals.jodis:
            Globals.jodis = Jodis(Manager())

    def user_resources(self, user_id):
        if not user_id:
            return {}

        resources = {}
        user = meta.Session.query(User).filter(User.id == user_id).first()
        accounts = meta.Session.query(Account).all()
        try:
            for account in accounts:
                if account.id in self.available_resources.keys() \
                        and (account.user_id == user.id \
                        or account.group_id in user.groups \
                        or (account.user_id is None and account.group_id is None)):
                    resources[account.id] = self.available_resources[account.id]
        except AttributeError:
            pass
        return resources

    @property
    def is_community_model(self):
        return pyconfig.get('cw.community_model_mode', 'true').lower() == 'true'

