from formalchemy.forms import FieldSet
from formalchemy.tables import Grid

from cyberweb import model
from cyberweb.model import meta

## Initialize fieldsets
GroupDefinition = FieldSet(model.GroupDefinition)
GroupDefinition.configure(pk=False,
                exclude=[GroupDefinition.members]
                )

GroupDefinitionAdd = FieldSet(model.GroupDefinition)
GroupDefinitionAdd.configure(pk=False,
                exclude=[GroupDefinitionAdd.members]
                )
## Initialize grids
GroupDefinitionGrid = Grid(model.GroupDefinition)
GroupDefinitionGrid.configure(pk=False,
                exclude=[GroupDefinitionGrid.members]
                )