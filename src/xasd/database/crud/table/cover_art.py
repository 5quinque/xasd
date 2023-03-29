import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import CoverArt as CoverArtModel


class CoverArt(Table):
    table = CoverArtModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = CoverArtModel.album
