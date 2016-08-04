from formalchemy.forms import FieldSet
from formalchemy.tables import Grid

from cyberweb import model
from cyberweb.model import meta

## Initialize fieldsets
Service = FieldSet(model.Service)
Service.configure(pk=False, exclude=[Service.timestamp])

ServiceAdd = FieldSet(model.Service)
ServiceAdd.configure(pk=False, exclude=[ServiceAdd.timestamp])
## Initialize grids
ServiceGrid = Grid(model.Service)
ServiceGrid.configure(pk=False, exclude=[ServiceGrid.timestamp])
