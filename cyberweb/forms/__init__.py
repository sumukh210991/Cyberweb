from pylons import config
from formalchemy import templates, validators, fields, forms, tables, config as fa_config

from cyberweb.model import meta
from cyberweb.lib.base import render
from cyberweb.forms.user import User, UserAdd, UserGrid
from cyberweb.forms.account import Account, AccountAdd, AccountGrid
from cyberweb.forms.group import Group, GroupAdd, GroupGrid
from cyberweb.forms.group_definition import GroupDefinition, GroupDefinitionAdd, GroupDefinitionGrid
from cyberweb.forms.service import Service, ServiceAdd, ServiceGrid
from cyberweb.forms.queue_info import QueueInfo, QueueInfoAdd, QueueInfoGrid

#if 'storage_path' in config['app_conf']:
#    # set the storage_path if we can find an options in app_conf
#    FileFieldRenderer.storage_path = config['app_conf']['storage_path']
#    ImageFieldRenderer.storage_path = config['app_conf']['storage_path']

fa_config.encoding = 'utf-8'

class TemplateEngine(templates.TemplateEngine):
    def render(self, name, **kwargs):
        return render('/forms/%s.mako' % name, extra_vars=kwargs)
fa_config.engine = TemplateEngine()

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

