from formalchemy.forms import FieldSet
from formalchemy.tables import Grid

from cyberweb import model
from cyberweb.model import meta

group_definitions = []
for i in meta.Session.query(model.GroupDefinition).all():
    group_definitions.append((i.name,i.id))
    
## Initialize fieldsets
User = FieldSet(model.User)
User.configure(pk=False,
                options=[User.groups.dropdown(options=group_definitions)],
                exclude=[User.password,User.last_login_date,User.created,User.last_login_ip,User.messages_sent,User.messages_by_user]
                )

UserAdd = FieldSet(model.User)
UserAdd.configure(pk=False,
                options=[UserAdd.groups.dropdown(options=group_definitions),
                         UserAdd.verified.checkbox()],
                exclude=[UserAdd.verified,UserAdd.password,UserAdd.last_login_date,UserAdd.created,UserAdd.last_login_ip,UserAdd.messages_sent,UserAdd.messages_by_user]
                )
## Initialize grids
group_definitions = []
for i in model.meta.Session.query(model.GroupDefinition).all():
    group_definitions.append((i.id,i.name))
UserGrid = Grid(model.User)
UserGrid.configure(pk=False,
                options=[UserGrid.groups.dropdown(options=group_definitions)],
                exclude=[UserGrid.password,UserGrid.last_login_date,UserGrid.created,UserGrid.last_login_ip,UserGrid.messages_sent,UserGrid.messages_by_user]
                )