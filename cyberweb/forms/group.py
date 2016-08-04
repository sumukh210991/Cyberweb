from formalchemy.forms import FieldSet
from formalchemy.tables import Grid

from cyberweb import model
from cyberweb.model import meta

## Initialize fieldsets
Group = FieldSet(model.Group)
Group.configure(pk=False,
                exclude=[Group.messages_by_group]
                )

GroupAdd = FieldSet(model.Group)
GroupAdd.configure(pk=False,
                exclude=[GroupAdd.messages_by_group]
                )
## Initialize grids
GroupGrid = Grid(model.Group)
GroupGrid.configure(pk=False,
                exclude=[GroupGrid.messages_by_group]
                )