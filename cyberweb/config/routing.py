"""
Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False
    map.append_slash = False
    

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/',controller='homepage',action='index')
    map.connect('/signin', controller='auth', action='signin')
    map.connect('/signout', controller='auth', action='signout')
    map.connect('/signup', controller='auth', action='signup')

    map.connect('/viz', controller='data', action='index', mako='/data/viz.mako')
    map.connect('/viz/download.tar.gz', controller='data', action='download', mako='/data/viz.mako')
    map.connect('/viz/{action}', controller='data', mako='/data/viz.mako')
    map.connect('/viz/{action}/{tablename}', controller='data', mako='/data/viz.mako')
    map.connect('/data/download.tar.gz', controller='data', action='download')

    map.connect('/test/basicjob',controller='basicjobs',action='index')
    map.connect('/postjob/{action}', controller='postjob', mako='/postjob/index.mako')
    
    # Map static files
    map.connect('fa_static', '/admin/_static/{path_info:.*}', controller='fa_admin', action='static')
    # Index page
    map.connect('admin', '/admin', controller='fa_admin', action='models')
    map.connect('formatted_admin', '/admin.json', controller='fa_admin', action='models', format='json')
    # Models
    map.resource('model', 'models', path_prefix='/admin/{model_name}', controller='fa_admin')
    
    map.connect('/{controller}', action='index')
    map.connect('/{controller}/', action='index')
    map.connect('/{controller}.wsdl')
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{tablename}')
    map.connect('/{controller}/{action}/{tablename}/{id}')

    return map
