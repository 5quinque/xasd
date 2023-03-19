import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Artist as ArtistModel


class Artist(Table):
    table = ArtistModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = ArtistModel.name
