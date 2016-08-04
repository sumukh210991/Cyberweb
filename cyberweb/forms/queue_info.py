from formalchemy.forms import FieldSet
from formalchemy.tables import Grid

from cyberweb import model
from cyberweb.model import meta

## Initialize fieldsets
QueueInfo = FieldSet(model.QueueInfo)
QueueInfo.configure(pk=False,
                exclude=[QueueInfo.timestamp]
                )

QueueInfoAdd = FieldSet(model.QueueInfo)
QueueInfoAdd.configure(pk=False,
                exclude=[QueueInfoAdd.timestamp]
                )
## Initialize grids
QueueInfoGrid = Grid(model.QueueInfo)
QueueInfoGrid.configure(pk=False,
                exclude=[QueueInfoGrid.timestamp]
                )