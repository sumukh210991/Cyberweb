from pylons import config
from formalchemy.forms import FieldSet
from formalchemy.tables import Grid

from cyberweb import model
from cyberweb.model import meta

users = []
for i in meta.Session.query(model.User).all():
    users.append((i.username,i.id))

Account = FieldSet(model.Account)
Account.configure(pk=False,
                      exclude=[Account.insert_date]
                     )

AccountAdd = FieldSet(model.Account)
AccountAdd.configure(pk=False,
                      exclude=[AccountAdd.insert_date]
                     )
## Initialize grids
AccountGrid = Grid(model.Account)
AccountGrid.configure(pk=False,
                      options=[AccountGrid.user.dropdown(options=users)],
                      exclude=[AccountGrid.authkey,AccountGrid.password,AccountGrid.insert_date]
                     )