import sqlalchemy

from xasd.database.crud.table import Table
from xasd.database.models import Genre as GenreModel


class Genre(Table):
    table = GenreModel

    def __init__(self, session: sqlalchemy.orm.session.Session):
        super().__init__(session)

        self.main_column = GenreModel.name
