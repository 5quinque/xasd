import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Album as AlbumModel


class Album(Table):
    table = AlbumModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = AlbumModel.name
