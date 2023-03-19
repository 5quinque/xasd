import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Track as TrackModel


class Track(Table):
    table = TrackModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = TrackModel.title
