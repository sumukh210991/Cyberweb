import logging
from formalchemy.ext.pylons.controller import ModelsController
from webhelpers.paginate import Page
from cyberweb.lib.base import BaseController, render
from cyberweb import model
from cyberweb import forms
from cyberweb.model import meta

log = logging.getLogger(__name__)

class AdminControllerBase(BaseController):
    model = model # where your SQLAlchemy mappers are
    forms = forms # module containing FormAlchemy fieldsets definitions
    def Session(self): # Session factory
        return meta.Session

    ## customize the query for a model listing
    # def get_page(self):
    #     if self.model_name == 'Foo':
    #         return Page(meta.Session.query(model.Foo).order_by(model.Foo.bar)
    #     return super(AdminControllerBase, self).get_page()

FaAdminController = ModelsController(AdminControllerBase,
                                   prefix_name='admin',
                                   member_name='model',
                                   collection_name='models',
                                  )
